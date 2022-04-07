#!/bin/bash
# **************************
# Localstack Boot Lambda
# Version: 1.0.0
# **************************
# -----------------------------------------------------------------------------
# Current file variables
# -----------------------------------------------------------------------------
debug=false
parent_folder="../"
current_path=$(pwd)/
current_path_basename=$(basename $(pwd))
current_file_full_path=$0
# echo $current_filepath
current_file_name=$(basename -- "$0")
# echo $current_filename
if [ $current_file_full_path = $current_file_name ] || [ $current_file_full_path = "./$current_file_name" ]; then
  current_file_full_path="./${current_file_full_path}"
  current_file_path="./"
else
  current_file_path="${current_file_full_path/$current_file_name/''}"
fi

current_file_path_basename=$(basename -- "$current_file_path")

if [ -z "$current_file_path_basename" ] || [ $current_file_path = "./" ]; then
#  echo 'aq'
  current_parent_folder="../"
else
#  echo 'naq'
  current_file_path_basename=$current_file_path_basename/
  current_parent_folder="${current_file_path/$current_file_path_basename/''}"
fi


if [ debug ]; then
  echo '----------------------------------------'
  echo "$0 - Script variables"
  echo '----------------------------------------'
  echo "current_path: $current_path"
  echo "current_path_basename: $current_path_basename"
  echo "current_file_full_path: $current_file_full_path"
  echo "current_file_name: $current_file_name"
  echo "current_file_path: $current_file_path"
  echo "current_parent_folder: $current_parent_folder"
  echo '----------------------------------------'
fi

echo '----------------------------------------'
echo "$0 - Booting lambda"
echo '----------------------------------------'
echo 'Installing dependencies...'
echo "Requirements file: ${current_parent_folder}requirements.txt"
if test -f ${current_parent_folder}requirements.txt; then
  python3 -m pip install -r ${current_parent_folder}requirements.txt -t ${current_parent_folder}vendor
  echo "requirements..."
fi

echo "Requirements file: ${current_parent_folder}requirements-vendor.txt"
if test -f ${current_parent_folder}requirements-vendor.txt; then
  python3 -m pip install -r ${current_parent_folder}requirements-vendor.txt -t ${current_parent_folder}vendor
  echo "requirements vendor..."
fi

echo 'Flask compatibility with Python 3.8'
python3 -m pip uninstall dataclasses -y
rm -Rf ${current_parent_folder}vendor/dataclasses-0.8.dist-info/ ${current_parent_folder}vendor/dataclasses.py

read -p "Press enter to continue..."

#echo 'Creating resource dependencies...'
#echo "${current_parent_folder}scripts/localstack/lambda/create-function-from-s3.sh"

if test -f "${current_parent_folder}scripts/localstack/lambda/create-function-from-s3.sh"; then

  if test -f ${current_parent_folder}.projectrc; then
    source ${current_parent_folder}.projectrc
  fi

  if [ -z "$APP_LAMBDA_NAME" ]; then
    echo 'APP_LAMBDA_NAME not defined'
    exit 1
  else
    echo '----------------------------------------'
    echo "$0 - Creating the lambda: $APP_LAMBDA_NAME"
    echo '----------------------------------------'
    ${current_parent_folder}scripts/localstack/lambda/create-function-from-s3.sh $current_filename_path $APP_LAMBDA_NAME $APP_LAMBDA_HANDLER

    read -p "Press enter to continue..."

    if test $APP_LAMBDA_EVENT_SOURCE = true;then
      if test $TEST_ENV = 0; then
        echo '----------------------------------------'
        echo "$0 - Creating the event source: $APP_LAMBDA_NAME"
        echo '----------------------------------------'
        ${current_parent_folder}scripts/localstack/lambda/create-event-source-mapping.sh $APP_LAMBDA_NAME $APP_QUEUE
      else
        echo 'Event source disabled'
      fi
    else
      echo 'There is no event source for this lambda'
    fi
  fi
else
  echo "File not found: ${current_parent_folder}scripts/localstack/lambda/create-function-from-s3.sh"
fi