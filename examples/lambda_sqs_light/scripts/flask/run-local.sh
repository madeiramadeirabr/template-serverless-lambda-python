#!/bin/bash
python3 -m venv venv
source ./venv/bin/activate

if test -f .projectrc; then
  source .projectrc
elif test -f ./scripts/.projectrc; then
  source ./scripts/.projectrc
fi

if [ "$1" = "--port" ]; then
  PORT=$2
fi
if [ -z "$PORT" ]; then
  if [ -z "$APP_PORT" ]; then
    PORT=5000
  else
    PORT=$APP_PORT
  fi
fi

echo "app port: $PORT"
export FLASK_ENV=development
export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run $1 $2
flask run --host=0.0.0.0 --port=$PORT