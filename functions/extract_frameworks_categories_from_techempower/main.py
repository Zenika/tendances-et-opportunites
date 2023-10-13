import functions_framework
import os
from google.cloud import secretmanager
from google.cloud import bigquery
import logging

from github import Auth
from github import Github
from github.GithubException import UnknownObjectException
import logging
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
DATASET_ID = "TechEmpower_frameworks"
TABLE_ID = "FRAMEWORKS"

def create_github():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "github_read_token"
    project_id = "tendances-tech-et-opportunites"
    request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
    response = client.access_secret_version(request)
    github_read_token = response.payload.data.decode("UTF-8")
    github = Github(auth=Auth.Token(github_read_token))
    return github

def list_frameworks_in_last_commit():
    """
    Lists all frameworks folders present in the last commit of the main branch of TechEmpower Frameworks repository
    Should return an array containing ... well, things?
    """
    repo = create_github().get_repo("TechEmpower/FrameworkBenchmarks")
    # Only get contents BELOW frameworks
    languages = repo.get_contents("frameworks")
    # Return value will be a list of default test results
    data = []
    # This folder contains only a list of folders, so explore them all
    for l in languages:
        logger.info("Searching below {}".format(l.path))
        frameworks = repo.get_contents(l.path)
        for f in frameworks:
            try:
                benchmark_config = repo.get_contents(f.path+"/benchmark_config.json")
                infos = json.loads(benchmark_config.decoded_content)
                to_add = infos["tests"][0]["default"]
                data.append(to_add)
            except UnknownObjectException as e:
                logger.error("Unable to get benchmark config for {}/{}".format(l.name, f.name))
    # Now we have all datas, can we make them simpler?
    # After all, we just want lists of
    # 1. Programming languages
    # 2. Web frameworks with the programming lanugages they can be used with
    return data

def create_frameworks_csv(frameworks_csv):
    fieldnames=  [
        "display_name","notes","framework","language","flavor","orm","platform","webserver","port","os","database","database_os",
        "db_url","query_url", "fortune_url","fortunes_url","update_url","plaintext_url","json_url","cached_query_url",
        "approach","classification","versus","network",
        "tags","cache","debug_port","setup_file","dockerfile"]
    writer = csv.DictWriter(frameworks_csv, fieldnames=fieldnames)
    writer.writeheader()
    for framework in list_frameworks_in_last_commit():
        try:
            writer.writerow(framework)
        except ValueError as e:
            logger.error("Unable to write row {} due to error {}".format(framework, e))
    # Those are all the TechEmpower fields
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
            bigquery.SchemaField("display_name", "STRING"),
            bigquery.SchemaField("notes", "STRING"),
            bigquery.SchemaField("framework", "STRING"),
            bigquery.SchemaField("language", "STRING"),
            bigquery.SchemaField("flavor", "STRING"),
            bigquery.SchemaField("orm", "STRING"),
            bigquery.SchemaField("platform", "STRING"),
            bigquery.SchemaField("webserver", "STRING"),
            bigquery.SchemaField("port", "INTEGER"),
            bigquery.SchemaField("os", "STRING"),
            bigquery.SchemaField("database", "STRING"),
            bigquery.SchemaField("database_os", "STRING"),
            bigquery.SchemaField("db_url", "STRING"),
            bigquery.SchemaField("query_url", "STRING"),
            bigquery.SchemaField("fortune_url", "STRING"),
            bigquery.SchemaField("fortunes_url", "STRING"),
            bigquery.SchemaField("update_url", "STRING"),
            bigquery.SchemaField("plaintext_url", "STRING"),
            bigquery.SchemaField("json_url", "STRING"),
            bigquery.SchemaField("cached_query_url", "STRING"),
            bigquery.SchemaField("approach", "STRING"),
            bigquery.SchemaField("classification", "STRING"),
            bigquery.SchemaField("versus", "STRING"),
            bigquery.SchemaField("network", "STRING"),
            bigquery.SchemaField("tags", "STRING"),
            bigquery.SchemaField("cache", "STRING"),
            bigquery.SchemaField("debug_port", "INTEGER"),
            bigquery.SchemaField("setup_file", "STRING"),
            bigquery.SchemaField("dockerfile", "STRING"),
        ],
    )

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    client = bigquery.Client()
    client.load_table_from_file(six.BytesIO(csv), table_id, 
        job_config=job_config).result()
    return "data imported"
