#!/bin/bash
if test -f .projectrc; then
  source .projectrc
elif test -f ./scripts/.projectrc; then
  source ./scripts/.projectrc
fi

if [ -z "$APP_NAME" ]; then
  echo 'APP_NAME not defined'
  exit 1
else
  zip -r $APP_NAME.zip ./ -x '*.git*' -x './zip.sh*' -x './venv/*' -x './.idea/*'  -x './node_modules/*'
fi
