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


if test -f "${current_filename_path}venv/bin/activate"; then
  source ${current_filename_path}venv/bin/activate
else
  python3 -m venv venv
fi

if test -f "${current_filename_path}scripts/install.sh"; then
  bash ${current_filename_path}scripts/install.sh
fi

if test -f "./scripts/tests/install-tests.sh"; then
  bash ./scripts/tests/install-tests.sh
fi