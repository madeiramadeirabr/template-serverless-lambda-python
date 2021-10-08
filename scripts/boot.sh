#!/bin/bash
# -----------------------------------------------------------------------------
# Current file variables
# -----------------------------------------------------------------------------
debug=false
parent_folder="../"
current_path=$(pwd)
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
if [ debug ]; then
  echo '----------------------------------------'
  echo "$0 - Script variables"
  echo '----------------------------------------'
  echo "current_path: $current_path"
  echo "current_path_basename: $current_path_basename"
  echo "current_file_full_path: $current_file_full_path"
  echo "current_file_name: $current_file_name"
  echo "current_file_path: $current_file_path"
  echo '----------------------------------------'
fi

echo '----------------------------------------'
echo "$0 - jq check"
echo '----------------------------------------'
echo 'Validating jq installation...'
/usr/bin/jq --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo 'Installing jq...'
  # download directly into ~/bin_compciv
  sudo curl http://stedolan.github.io/jq/download/linux64/jq -o /usr/bin/jq
  # give it executable permissions
  sudo chmod a+x /usr/bin/jq
else
  echo 'jq installed...'
fi


echo '----------------------------------------'
echo "$0 - Localstack connection check"
echo '----------------------------------------'
# valida se o Localstack está rodando
if test -f ${current_file_path}boot-validate-connection.sh; then
  echo 'Validate connection...'
  ${current_file_path}boot-validate-connection.sh
else
  echo 'There is no connection check'
fi


echo '----------------------------------------'
echo "$0 - Database boot"
echo '----------------------------------------'
if test -f ${current_file_path}boot-db.sh; then
  ${current_file_path}boot-db.sh
else
  echo 'There is no database to be booted'
fi

echo '----------------------------------------'
echo "$0 - Queues boot"
echo '----------------------------------------'
if test -f ${current_file_path}boot-queues.sh; then
  ${current_file_path}boot-queues.sh
else
  echo 'There is no queues to be booted'
fi

echo '----------------------------------------'
echo "$0 - Lambdas boot"
echo '----------------------------------------'
if test -f ${current_file_path}boot-lambdas.sh; then
  ${current_file_path}boot-lambdas.sh
else
  echo 'There is no lambdas to be booted'
fi