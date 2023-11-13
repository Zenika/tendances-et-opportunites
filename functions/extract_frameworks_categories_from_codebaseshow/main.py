import functions_framework
import os
from google.cloud import secretmanager
from google.cloud import bigquery
import logging
import requests
from jinja2 import Environment, PackageLoader, select_autoescape

import sys
import json
import csv
import io
import six

# setup logging
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
# Formatter kindly provided by https://stackoverflow.com/a/69767482/15619
# formatter = CloudLoggingFormatter(fmt="[%(name)s] %(message)s")
# handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

PROJECT_ID = "tendances-tech-et-opportunites"
DATASET_ID = "Codebaseshow_frameworks"
TABLE_ID = "FRAMEWORKS"

jinja = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

def get_applications_payload():
    text = jinja.get_template("applications.json")
    return json.loads(text.render())

def get_implementations_payload(id, category):
    text = jinja.get_template("implementations.json")
    return json.loads(text.render(id=id, category=category))

def list_implementations_of(application):
    logger.info("Reading implementations of %s", application)
    all_implementations = []
    for category in application['categories']:
        payload = get_implementations_payload(application['id'], category)
        implementations_response = requests.post("https://backend.codebase.show/",
            json=payload
        )
        if implementations_response.status_code<300:
            implementations = implementations_response.json()
            all_implementations = all_implementations + implementations['result']
    return all_implementations

def list_current_frameworks():
    """
    List available frameworks by
    1. Getting all applications
    2. For each application, getting all implementations
    3. Sorting results by language, then side (backend, frontend, full stack), then framework
    """
    payload = get_applications_payload()
    applications_response = requests.post("https://backend.codebase.show/",
        json=payload
    )
    if applications_response.status_code<300:
        applications = applications_response.json()
        all_implementations = []
        for application in applications['result']:
            implementations = list_implementations_of(application)
            all_implementations = all_implementations + implementations
        return all_implementations
    else:
        raise ValueError(f"Unable to get list of applications due to {applications_response.content}\npayload is\n{payload}")

def create_frameworks_csv(frameworks_csv):
    fieldnames=  [
        "language","framework",
        "frontendEnvironment","libraries", "repositoryURL"]
    writer = csv.DictWriter(frameworks_csv, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    frameworrks = list_current_frameworks()
    for framework in frameworrks:
        try:
            if isinstance(framework['frontendEnvironment'], dict):
                framework['frontendEnvironment'] = "web"
            framework['framework'] = framework['libraries'].pop(0)
            writer.writerow(framework)
        except ValueError as e:
            logger.error("Unable to write row {} due to error {}".format(framework, e))
    # Those are all the CodebaseShow fields
#    table = bigquery.Table(f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", schema=schema)
#    table = client.create_table(table)

@functions_framework.http
def http_function(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    file = "frameworks.csv"
    csv = ""
    if not os.path.exists(file):
        with open(file, "w", newline='') as fd:
            create_frameworks_csv(fd)
    with open(file, "rb") as fd:
        csv = fd.read()

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=[
            bigquery.SchemaField("language", "STRING"),
            bigquery.SchemaField("framework", "STRING"),
            bigquery.SchemaField("frontendEnvironment", "STRING"),
            bigquery.SchemaField("libraries", "STRING"),
            bigquery.SchemaField("repositoryURL", "STRING"),
        ],
    )

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    client = bigquery.Client()
    client.load_table_from_file(six.BytesIO(csv), table_id, 
        job_config=job_config).result()
    return "data imported"
