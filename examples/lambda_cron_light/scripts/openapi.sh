#!/bin/bash
if test -f ./openapi/generate-openapi.py; then
  python3 ./openapi/generate-openapi.py
elif test -f ./scripts/openapi/generate-openapi.py; then
  python3 ./scripts/openapi/generate-openapi.py
else
  echo 'generate-openapi.py not found'
  exit 1
fi