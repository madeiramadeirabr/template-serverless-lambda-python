#!/bin/bash

## variables
source ${current_filename_path}scripts/variables.sh

## now loop through the above array
for example_path in "${arr[@]}"
do
   echo "Installing data for ${example_path}"
   if test -f "${example_path}requirements.txt"; then
     python3 -m pip install -r ${example_path}requirements.txt
   fi

   if test -f "${example_path}requirements-vendor.txt"; then
    python3 -m pip install -r ${example_path}requirements-vendor.txt -t ./${example_path}vendor
   fi
done

# You can access them using echo "${arr[0]}", "${arr[1]}" also
