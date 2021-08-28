#!/bin/bash

# declare an array variable
declare -a arr=("./examples/lambda_api/" "./examples/lambda_cron/" "./examples/lambda_s3/" "./examples/lambda_sns/" "./examples/lambda_sqs/")

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
