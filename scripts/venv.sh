#!/bin/bash
#python3 -m venv venv
#source ./venv/bin/activate
mkvirtualenv lambda_fAPI

if test -f "./scripts/install.sh"; then
  bash ./scripts/install.sh
fi
