#!/bin/bash
current_path=$(basename $(pwd))
current_filename=$(basename -- "$0")
current_filename_path=$0
# echo $current_filename_path
current_filename_path="${current_filename_path/$current_filename/''}"
# echo $current_filename_path
current_filename_path="${current_filename_path/scripts\//''}"
# echo $current_filename_path
current_filename_path_basename=$(basename -- "$current_filename_path")

echo "current_path: $current_path"
echo "current_filename: $current_filename"
echo "current_filename_path: $current_filename_path"
echo "current_filename_path_basename: $current_filename_path_basename"

if test -f ${current_filename_path}/scripts/localstack/sqs/create-queue.sh; then

  if test -f ${current_filename_path}.projectrc; then
    source ${current_filename_path}.projectrc
  fi

  if [ -z "$APP_QUEUE" ]; then
    echo 'APP_QUEUE not defined'
    exit 1
  else
    echo "Creating the queue: $APP_QUEUE"
    ${current_filename_path}/scripts/localstack/sqs/create-queue.sh $APP_QUEUE
  fi
fi

