# TechEmpower categories extractor

This cloud function simply extracts the various available web frameworks from TechEmpower Frmaeworks GitHub repository.

Triggered by a Google Cron, it writes a Big Query table mapping the languages/frameworks onto Stackoverflow associated tags.


## How to install

### Install functions framework on Windows

`sudo pip install functions-framework`

(the sudo is here to have functions framework available on Windows path)

### Install other dependencies

`pip install -r requirements --user`

### Install Google Cloud Function

**Should only be done once**
`gcloud init`

### Deploy function code
(borrowed from [Deploy a function](https://cloud.google.com/functions/docs/create-deploy-gcloud))
```
gcloud functions deploy extract-framework-categories-from-techempower --gen2 --runtime=python311 --region=us-west1 --source=. --entry-point=http_function --trigger-http --allow-unauthenticated
```

## How to run locally

`functions-framework --target hello_http --debug`

## How to invoke/test

Run tests using `python -m pytest`

Start function locally with `functions_framework --target http_function --debug`

## How to change the GitHub auth token

```
echo "LE TOKEN" | gcloud secrets create github_read_token --data-file=- --replication-policy=automatic
```

### Allow Google Cloud Function to access secret

```
gcloud secrets add-iam-policy-binding github_read_token --role roles/secretmanager.secretAccessor  --member serviceAccount:tendances-tech-et-opportunites@appspot.gserviceaccount.com
```