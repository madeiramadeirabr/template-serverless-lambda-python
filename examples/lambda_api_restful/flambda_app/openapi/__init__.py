"""
OpenAPI Module for Flambda APP
Version: 1.0.0
"""
import os

import yaml
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from flambda_app import APP_NAME, APP_VERSION
# Create an APISpec
from flambda_app.config import get_config
from flambda_app.helper import open_vendor_file, get_environment
from flambda_app.logging import get_logger

env = get_environment()

servers = [
    {
        "url": os.environ["API_SERVER"] if "API_SERVER" in os.environ else None,
        "description": os.environ["API_SERVER_DESCRIPTION"] if "API_SERVER_DESCRIPTION" in os.environ else None
    }
]

if env == "development":
    servers.append({
        "url": os.environ["LOCAL_API_SERVER"] if "LOCAL_API_SERVER" in os.environ else "http://localhost:5000",
        "description": os.environ["LOCAL_API_SERVER_DESCRIPTION"]
        if "LOCAL_API_SERVER_DESCRIPTION" in os.environ
        else "Development server"
    })


spec = APISpec(
    title=APP_NAME,
    openapi_version='3.0.2',
    version=APP_VERSION,
    plugins=[
        MarshmallowPlugin()
    ],
    servers=servers
)


def generate_openapi_yml(spec_object, logger, force=False):
    try:
        openapi_data = spec_object.to_yaml()

        if os.environ['APP_ENV'] == 'development' or force:
            stream = open_vendor_file("./public/swagger/openapi.yml", "w")

            if stream:
                stream.write(openapi_data)
                stream.close()
    except Exception as err:
        logger.error(err)


# doc
def get_doc(fn):
    logger = get_logger()
    doc_yml = ''
    try:

        fn_doc = fn.__doc__
        if fn_doc:
            fn_doc = fn_doc.split('---')[-1]
            doc_yml = yaml.safe_load(fn_doc)
    except Exception as err:
        logger.error(err)
    return doc_yml
