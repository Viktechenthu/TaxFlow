#!/bin/bash

case "$1" in
  dev)
    echo "Starting development server..."
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ;;
  prod)
    echo "Starting production server..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    ;;
  test)
    echo "Running tests..."
    pytest
    ;;
  *)
    echo "Usage: ./run.sh {dev|prod|test}"
    ;;
esac
