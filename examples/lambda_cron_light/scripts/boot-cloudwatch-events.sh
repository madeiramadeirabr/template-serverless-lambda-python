#!/bin/bash
# -----------------------------------------------------------------------------
# Current file variables
# -----------------------------------------------------------------------------
debug=0
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
#echo "xxxxx current_file_path_basename $current_file_path_basename"

if [ -z "$current_file_path_basename" ] || [ $current_file_path = "./" ]; then
#  echo 'aq'
  current_parent_folder="../"
else
#  echo 'naq'
  current_file_path_basename=$current_file_path_basename/
  current_parent_folder="${current_file_path/$current_file_path_basename/''}"
fi


if [[ $debug == 1 ]]; then
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

if test -f ${current_parent_folder}/scripts/localstack/cloudwatch/put-rule.sh; then

#  echo "${current_parent_folder}.projectrc"
  if test -f ${current_parent_folder}.projectrc; then
    source ${current_parent_folder}.projectrc
  fi

  if [ -z "$APP_RULE_NAME" ]; then
    echo 'APP_RULE_NAME not defined'
    exit 1
  else
    echo "Creating the rule: $APP_RULE_NAME"
    ${current_parent_folder}scripts/localstack/cloudwatch/put-rule.sh $APP_RULE_NAME $APP_RULE_EXPRESSION_TYPE "$APP_RULE_EXPRESSION" $APP_REGION
  fi
fi
