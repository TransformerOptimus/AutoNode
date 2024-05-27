#!/bin/bash

# Run Alembic migrations
alembic -c autonode/alembic.ini upgrade heads

# Start the app
exec uvicorn autonode.app:app --host 0.0.0.0 --port 8001 --reload