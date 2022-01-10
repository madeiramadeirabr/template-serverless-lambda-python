#!/bin/bash
if test -f .projectrc; then
  source .projectrc
elif test -f ./scripts/.projectrc; then
  source ./scripts/.projectrc
fi

if [ -z "$PROJECT_NAME" ]; then
  echo 'PROJECT_NAME not defined'
  exit 1
else
  docker-compose exec $PROJECT_NAME /bin/sh
fi
