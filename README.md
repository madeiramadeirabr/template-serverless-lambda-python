# template-serverless-lambda-python
This project contains isolated examples of AWS Lambda Services as well this provide
a stack example.

## Service Architecture
Example of architecture of this project stack.
![Service-Arch](docs/service-stack.png)

## Single projects
You can find single examples for:
* [Lambda API](./examples/lambda_api)
* [Lambda CRON](./examples/lambda_cron)
* [Lambda SQS](./examples/lambda_sqs)
* [Lambda SNS](./examples/lambda_sns)
* [Lambda S3](./examples/lambda_s3)


## Stack
* AWS Lambda
* Flask for APIs
* Custom code based in AWS Chalice for SQS, SNS, S3 and CRON

## Prerequisites
* Docker
* Docker-compose
* Python 3.x

## Installation
### Creating the virtual env
To create the venv and install the modules execute:
```bash
./scripts/venv.sh
```

### Running via docker
To execute the build:
```bash
./scripts/runenv.sh --build
```
Execute the follow command:
```bash
./scripts/runenv.sh
```
### Boot the resources
Execute the follow command:
```bash
./scripts/boot.sh
```
