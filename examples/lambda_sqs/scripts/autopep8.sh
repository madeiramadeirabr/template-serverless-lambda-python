#!/bin/bash
if [ -z "$1" ]; then
#  autopep8 --in-place --recursive --aggressive
  autopep8 --global-config .pep8 --in-place --recursive --verbose ./app.py ./boot.py
  if test -d ./lambda_app; then
    autopep8 --global-config .pep8 --in-place --recursive --verbose ./lambda_app
  fi
  if test -d ./flambda_app; then
    autopep8 --global-config .pep8 --in-place --recursive --verbose ./flambda_app
  fi
  if test -d ./chalicelib; then
    autopep8 --global-config .pep8 --in-place --recursive --verbose ./chalicelib
  fi

else
  autopep8 --global-config .pep8 --in-place --aggressive --verbose $1
fi
