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
#echo $current_file_full_path
#echo $current_file_name
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


## variables
echo '----------------------------------------'
echo "$0 - Sourcing file: ${current_file_path}variables.sh"
echo '----------------------------------------'
source ${current_file_path}variables.sh

## now loop through the above array
for example_path in "${arr[@]}"
do
   echo "Booting ${example_path} ..."
   if test -f "${parent_folder}${example_path}scripts/boot.sh"; then
     ${parent_folder}${example_path}scripts/boot.sh
   elif test -f "${example_path}scripts/boot.sh"; then
     ${example_path}scripts/boot.sh
   else
     echo 'There is no boot file'
   fi
done

# You can access them using echo "${arr[0]}", "${arr[1]}" also