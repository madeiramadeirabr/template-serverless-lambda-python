"""This is the main file of the lambda application

This module contains the handler method
"""
import base64
import os

import boot
from lambda_app import APP_NAME, APP_VERSION, http_helper
from lambda_app import helper
from lambda_app.config import get_config
from lambda_app.enums.messages import MessagesEnum
from lambda_app.exceptions import ApiException
from lambda_app.helper import open_vendor_file, print_routes
from lambda_app.http_helper import CUSTOM_DEFAULT_HEADERS
from lambda_app.http_resources.request import ApiRequest
from lambda_app.http_resources.response import ApiResponse
from lambda_app.lambda_flask import LambdaFlask
from lambda_app.logging import get_logger
from lambda_app.openapi import spec, get_doc, generate_openapi_yml
from lambda_app.services.product_manager import ProductManager
from lambda_app.services.v1.healthcheck import HealthCheckResult
from lambda_app.services.v1.healthcheck.resources import \
    MysqlConnectionHealthCheck, RedisConnectionHealthCheck, \
    SQSConnectionHealthCheck, SelfConnectionHealthCheck
from lambda_app.services.v1.healthcheck_service import HealthCheckService
from lambda_app.services.v1.product_service import ProductService as ProductServiceV1

# load env
ENV = helper.get_environment()
boot.load_dot_env(ENV)

# config
CONFIG = get_config()
# debug
DEBUG = helper.debug_mode()
# logger
LOGGER = get_logger()

APP = LambdaFlask(__name__)


@APP.route('/')
def index():
    """
    API Root path
    :return:
    :rtype: str
    """
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    return http_helper.create_response(body=body, status_code=200)


# general vars
APP_QUEUE = CONFIG.APP_QUEUE


@APP.route('/alive')
def alive():
    """
    Health check path
    :return:
    :rtype: str

    ---

        get:
            summary: Service Health Method
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: HealthCheckSchema
        """
    service = HealthCheckService()
    service.add_check("self", SelfConnectionHealthCheck(LOGGER, CONFIG), [])
    service.add_check(
        "mysql", MysqlConnectionHealthCheck(LOGGER, CONFIG), ["db"])
    service.add_check("redis", RedisConnectionHealthCheck(
        LOGGER, CONFIG), ["redis"])
    service.add_check("queue", SQSConnectionHealthCheck(
        LOGGER, CONFIG), ["queue"])
    service.add_check("test", lambda: HealthCheckResult.unhealthy("connected"), ["example"])
    service.add_check("test2", lambda: HealthCheckResult.unhealthy("connected"), ["example"])

    return service.get_response()


@APP.route('/favicon-32x32.png')
def favicon():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "image/png"
    data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAkFBMVEUAAAAQM0QWNUYWNkYXNkYALjo'
        'WNUYYOEUXN0YaPEUPMUAUM0QVNUYWNkYWNUYWNUUWNUYVNEYWNkYWNUYWM0eF6i0XNkchR0OB5SwzZj'
        '9wyTEvXkA3az5apTZ+4C5DgDt31C9frjU5bz5uxTI/eDxzzjAmT0IsWUEeQkVltzR62S6D6CxIhzpKi'
        'jpJiDpOkDl4b43lAAAAFXRSTlMAFc304QeZ/vj+ECB3xKlGilPXvS2Ka/h0AAABfklEQVR42oVT2XaC'
        'MBAdJRAi7pYJa2QHxbb//3ctSSAUPfa+THLmzj4DBvZpvyauS9b7kw3PWDkWsrD6fFQhQ9dZLfVbC5M'
        '88CWCPERr+8fLZodJ5M8QJbjbGL1H2M1fIGfEm+wJN+bGCSc6EXtNS/8FSrq2VX6YDv++XLpJ8SgDWM'
        'nwqznGo6alcTbIxB2CHKn8VFikk2mMV2lEnV+CJd9+jJlxXmMr5dW14YCqwgbFpO8FNvJxwwM4TPWPo'
        '5QalEsRMAcusXpi58/QUEWPL0AK1ThM5oQCUyXPoPINkdd922VBw4XgTV9zDGWWFrgjIQs4vwvOg6xr'
        '+6gbCTqE+DYhlMGX0CF2OknK5gQ2JrkDh/W6TOEbYDeVecKbJtyNXiCfGmW7V93J2hDus1bDfhxWbIZ'
        'VYDXITA7Lo6E0Ktgg9eB4KWuR44aj7ppBVPazhQH7/M/KgWe9X1qAg8XypT6nxIMJH+T94QCsLvj29I'
        'YwZxyO9/F8vCbO9tX5/wDGjEZ7vrgFZwAAAABJRU5ErkJggg==')
    return http_helper.create_response(
        body=data, status_code=200, headers=headers)


@APP.route('/docs')
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/html"
    html_file = open_vendor_file('./public/swagger/index.html', 'r')
    html = html_file.read()
    return http_helper.create_response(
        body=html, status_code=200, headers=headers)


@APP.route('/openapi.yml')
def openapi():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/yaml"
    html_file = open_vendor_file('./public/swagger/openapi.yml', 'r')
    html = html_file.read()
    return http_helper.create_response(
        body=html, status_code=200, headers=headers)


@APP.route('/v1/product', methods=['GET'])
def product_list():
    """
    ---
    get:
        summary: Product List
        parameters:
            - name: limit
              in: query
              description: "List limit"
              required: false
              schema:
                type: int
                example: 20
            - name: offset
              in: query
              description: "List offset"
              required: false
              schema:
                type: int
                example: 0
            - name: fields
              in: query
              description: "Filter fields with comma"
              required: false
              schema:
                type: string
                example:
            - name: order_by
              in: query
              description: "Ordination of list"
              required: false
              schema:
                type: string
                enum:
                 - "asc"
                 - "desc"
            - name: sort_by
              in: query
              description: "Sorting of the list"
              required: false
              schema:
                type: string
                example: id
        responses:
            200:
                description: Success response
                content:
                    application/json:
                        schema: ProductListResponseSchema
    """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('request: {}'.format(request))

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(True)

    manager = ProductManager(logger=LOGGER, product_service=ProductServiceV1(logger=LOGGER))
    manager.debug(DEBUG)
    try:
        response.set_data(manager.list(request))
        response.set_total(manager.count(request))
    except Exception as err:
        LOGGER.error(err)
        LOGGER.info('aq')
        error = ApiException(MessagesEnum.LIST_ERROR)
        status_code = 400
        if manager.exception:
            error = manager.exception
        response.set_exception(error)

    return response.get_response(status_code)


@APP.route('/v1/product/<uuid>', methods=['GET'])
def product_get(uuid):
    pass


@APP.route('/v1/product/<uuid>', methods=['POST'])
def product_create():
    pass


@APP.route('/v1/product/<uuid>', methods=['PUT'])
def product_update():
    pass


@APP.route('/v1/product/<uuid>', methods=['DELETE'])
def product_delete():
    pass


# *************
# doc
# *************
spec.path(view=alive, path="/alive", operations=get_doc(alive))
# *************
# product
# *************
spec.path(view=product_list,
          path="/v1/product", operations=get_doc(product_list))
spec.path(view=product_get,
          path="/v1/product/{uuid}", operations=get_doc(product_get))
spec.path(view=product_create,
          path="/v1/product/{uuid}", operations=get_doc(product_create))
spec.path(view=product_update,
          path="/v1/product/{uuid}", operations=get_doc(product_update))
spec.path(view=product_delete,
          path="/v1/product/{uuid}", operations=get_doc(product_delete))

print_routes(APP, LOGGER)
LOGGER.info('Running at {}'.format(os.environ['APP_ENV']))

# *************
# generate de openapi.yml
# *************
generate_openapi_yml(spec, LOGGER, force=True)
