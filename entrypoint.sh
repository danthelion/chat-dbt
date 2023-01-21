#!/bin/bash

set -eu

# check if weaviate is running (change to localhost if you run outside Docker)
until curl http://weaviate:8080/v1/.well-known/live; do sleep 1; done

python3 ingest.py && python3 ingest_examples.py && python3 app.py
