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
  python3 -m venv venv
  source ${current_filename_path}venv/bin/activate
else
  echo "Unable to find  ${current_filename_path}venv/bin/activate"
  exit 1
fi

if test -f "$1"; then
  bash $1
else
  echo "Unable to find  $1"
  exit 1
fi
