# install requirements
#cd ./shark-tank-rules-manager
#python3 -m pip install -r ./requirements.txt -t ./vendor
#python3 -m pip install -r ./requirements-vendor.txt -t ./vendor
#cd ../
#
#
## create resource dependencies
#./bin/localstack/lambda/create-function-from-s3.sh shark-tank-rules-manager
#./bin/localstack/lambda/create-event-source-mapping.sh shark-tank-rules-manager shark-tank-rules-manager-queue
#
## install requirements
#cd ./sourcing-service-rules-processor
#python3 -m pip install -r ./requirements.txt -t ./vendor
#python3 -m pip install -r ./requirements-vendor.txt -t ./vendor
#cd ../
#
## create resource dependencies
#./bin/localstack/lambda/create-function-from-s3.sh sourcing-service-rules-processor
#./bin/localstack/lambda/create-event-source-mapping.sh sourcing-service-rules-processor sourcing-service-events-api-staging-rules-queue
#
## sourcing-service-decision-processor
##cd ./sourcing-service-decision-processor
##python3 -m pip install -r ./requirements.txt -t ./vendor
##python3 -m pip install -r ./requirements-vendor.txt -t ./vendor
### temp
###python3 -m pip install -r ./requirements-tests.txt -t ./vendor
##cd ../
#
## create resource dependencies
##./bin/localstack/lambda/create-function-from-s3.sh sourcing-service-decision-processor sourcing-service-decision-processor-sale-event app.handle_sales_event_sqs
##./bin/localstack/lambda/create-event-source-mapping.sh sourcing-service-decision-processor-sale-event sourcing-service-events-api-staging-sales-event-queue
##
##./bin/localstack/lambda/create-function-from-s3.sh sourcing-service-decision-processor-decision-event app.handle_decision_event_sqs
##./bin/localstack/lambda/create-event-source-mapping.sh sourcing-service-decision-processor-sale-event sourcing-service-events-api-staging-decision-queue
##