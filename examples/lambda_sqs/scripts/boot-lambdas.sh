echo 'Booting lambda...'
echo 'Installing dependencies...'
# ./scripts/venv.sh
python3 -m pip install -r ./requirements.txt -t ./vendor
python3 -m pip install -r ./requirements-vendor.txt -t ./vendor

echo 'Creating resource dependencies...'
## create resource dependencies
./scripts/localstack/lambda/create-function-from-s3.sh lambda_sqs
./scripts/localstack/lambda/create-event-source-mapping.sh lambda_sqs test-queue