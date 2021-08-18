FROM python:3.8.11-alpine3.13
MAINTAINER Anderson Contreira <anderson.contreira@gmail.com>

ARG PROJECT_NAME=template-serverless-lambda-python
ARG FLASK_PORT=5000
ARG ENVIRONMENT_NAME=development
ENV FLASK_ENV=$ENVIRONMENT_NAME \
    FLASK_APP=app.py

EXPOSE ${FLASK_PORT}

WORKDIR /${PROJECT_NAME}

# SQLite support
RUN apk update \
    && apk add sqlite \
    && apk add socat

# gcc requirement for greenlit and sqlalchemy
RUN apk add --no-cache build-base \
                       python3-dev \
                       libffi-dev \
                       musl-dev \
                       make \
                       gcc \
                       openldap \
                       libcurl \
                       gpgme-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*

# upgrade pip
RUN pip install --upgrade pip

# Install requirements
COPY requirements.txt requirements-vendor.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-vendor.txt

# Copy project files
COPY . .

#CMD [ "flask", "run", "--host", "0.0.0.0" ]
CMD [ "python3", "server.py" ]

