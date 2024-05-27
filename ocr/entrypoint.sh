#!/bin/sh

gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8001