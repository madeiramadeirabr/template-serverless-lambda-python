#!/bin/bash
if [ -z "$1" ]; then
  pylint --rcfile .pylint ./app.py ./boot.py
  if test -d ./lambda_app; then
    pylint --rcfile .pylint ./lambda_app
  fi
  if test -d ./flambda_app; then
    pylint --rcfile .pylint ./flambda_app
  fi
  if test -d ./chalicelib; then
    pylint --rcfile .pylint ./chalicelib
  fi

else
  pylint --rcfile .pylint $1
fi
