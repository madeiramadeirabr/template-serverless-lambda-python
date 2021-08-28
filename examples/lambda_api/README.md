# template-serverless-lambda-python - Lambda API
Template for build flexible API with AWS Lambda.

## Service Architecture
Example of architecture with Kong API Gateway.
![Service-Arch](docs/service-arch.png)

## General Service Routes Architecture
Service routes map.
![Service-Routes](docs/service-routes.png)

# Prerequisites
- Python 3.6
- docker
- docker-compose
- python-dotenv
- jsonformatter
- requests
- pytz
- redis
- pyyaml
- apispec
- marshmallow
- Flask

## Features
- Docker-compose 
- OpenApi
- SQS Integration
* Flask
* MySQL
* Redis
* Swagger

## Installation

### Running Locally
To create the `venv` and install the modules execute:
```
./scripts/venv.sh
```
#### Running the app
Execute the follow command:
```
./scripts/flask/run-local.sh
```
### Running via docker
To execute the build:
```
./bin/runenv.sh --build
```

Execute the follow command:
```
./bin/runenv.sh
```

### Boot the queues
Execute the follow command:
```
./bin/boot.sh
```

## Samples
See the project samples in this folder [here](samples).

## Running tests
To run the unit tests of the project you can execute the follow command:

First you need install the tests requirements:
 ```
 ./bin/venv-exec.sh ./bin/tests/install-tests.sh 
 ```

 
### Unit tests:
 ```
./bin/venv-exec.sh ./bin/tests/unit-tests.sh
 ``` 
### Components tests:
Start the docker containers:
 ```
./bin/runenv.sh
```
Booting the environment:
 ```
./bin/boot.sh
```

Executing the tests:
 ```
./bin/venv-exec.sh ./bin/tests/component-tests.sh
```
### Integration tests:
Copy the file `config/integration.env.example` to 
`config/integration.env` and edit it with de staging parameters.

Executing the tests:
 ```
./bin/venv-exec.sh ./bin/tests/integration-tests.sh
```


### All tests:
Executing the tests:
```
 ./bin/venv-exec.sh ./bin/tests/tests.sh 
 ```

## Generating coverage reports
To execute coverage tests you can execute the follow commands:

### Unit test coverage:
Execute the follow command:
``` 
./bin/venv-exec.sh ./bin/tests/unit-coverage.sh
``` 

### Component test coverage:
Start the docker containers:
``` 
./bin/runenv.sh
```
Booting the environment:
 ```
./bin/boot.sh
```

Execute the follow command:
``` 
./bin/venv-exec.sh ./bin/tests/component-coverage.sh
```

### Integration test coverage:

Copy the file `config/integration.env.example` to 
`config/integration.env` and edit it with de staging parameters.

Execute the follow command:
``` 
./bin/venv-exec.sh ./bin/tests/integration-coverage.sh
```
> Observation:

The result can be found in the folder `target/*`.


## License
See the license [LICENSE.md](LICENSE.md).

## Contributions
* Anderson de Oliveira Contreira [andersoncontreira](https://github.com/andersoncontreira)

