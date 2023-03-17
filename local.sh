#!/bin/bash


source venv/bin/activate
export BBP_NEXUS_ENDPOINT="https://bbp.epfl.ch/nexus/v1"
export ENVIRONMENT="LOCAL"
export RULES_BUCKET="bbp/inference-rules"
export DATAMODELS_BUCKET="neurosciencegraph/datamodels"
export WHITELISTED_CORS_URLS="http://api:8000"
export NEXUS_TOKEN=""

if $1 = "--test"
then
  pytest api/test.py -W ignore::DeprecationWarning
else
  uvicorn api.main:app --host 0.0.0.0 --port 8080
fi