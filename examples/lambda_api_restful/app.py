"""This is the main file of the lambda application

This module contains the handler method
"""
import base64
import os

import boot
from flambda_app import APP_NAME, APP_VERSION, http_helper
from flambda_app import helper
from flambda_app.config import get_config
from flambda_app.enums.events import EventType
from flambda_app.enums.messages import MessagesEnum
from flambda_app.events.tracker import EventTracker
from flambda_app.exceptions import ApiException, ValidationException
from flambda_app.flambda import Flambda
from flambda_app.helper import open_vendor_file, print_routes
from flambda_app.http_helper import CUSTOM_DEFAULT_HEADERS, set_hateos_links, set_hateos_meta
from flambda_app.http_resources.request import ApiRequest
from flambda_app.http_resources.response import ApiResponse
from flambda_app.logging import get_logger, set_debug_mode
from flambda_app.openapi import spec, get_doc, generate_openapi_yml
from flambda_app.services.event_manager import EventManager
from flambda_app.services.healthcheck_manager import HealthCheckManager
from flambda_app.services.product_manager import ProductManager
from flambda_app.services.v1.ocoren_event_service import OcorenEventService
from flambda_app.services.v1.product_service import ProductService as ProductServiceV1
from flambda_app.openapi import api_schemas

# load directly by boot
from flambda_app.vos.events import EventVO

ENV = boot.get_environment()
# boot.load_dot_env(ENV)


# config
CONFIG = get_config()
# debug
DEBUG = helper.debug_mode()

# keep in this order, the app generic stream handler will be removed
APP = Flambda(APP_NAME)
# Logger
LOGGER = get_logger()
# override the APP logger
APP.logger = LOGGER
# override the log configs
if DEBUG:
    # override to the level desired
    set_debug_mode(LOGGER)

API_ROOT = os.environ['API_ROOT'] if 'API_ROOT' in os.environ else None
API_ROOT_ENDPOINT = API_ROOT if API_ROOT != "" else '/'


@APP.route(API_ROOT_ENDPOINT)
def index():
    """
    API Root path
    :return:
    :rtype: str
    """
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    return http_helper.create_response(body=body, status_code=200)


@APP.route(API_ROOT + '/alive')
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
                424:
                    description: Failed dependency response
                    content:
                        application/json:
                            schema: HealthCheckSchema
                503:
                    description: Service unavailable response
                    content:
                        application/json:
                            schema: HealthCheckSchema
        """
    service = HealthCheckManager()
    return service.check()


@APP.route(API_ROOT + '/favicon-32x32.png')
def favicon():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "image/png"
    data = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAkFBMVEUAAAAQM0QWNUYWNkYXNkYALjoWNUYYOEUXN0YaPEUPMUAUM0QVN' \
           'UYWNkYWNUYWNUUWNUYVNEYWNkYWNUYWM0eF6i0XNkchR0OB5SwzZj9wyTEvXkA3az5apTZ+4C5DgDt31C9frjU5bz5uxTI/eDxzzjAmT0' \
           'IsWUEeQkVltzR62S6D6CxIhzpKijpJiDpOkDl4b43lAAAAFXRSTlMAFc304QeZ/vj+ECB3xKlGilPXvS2Ka/h0AAABfklEQVR42oVT2Xa' \
           'CMBAdJRAi7pYJa2QHxbb//3ctSSAUPfa+THLmzj4DBvZpvyauS9b7kw3PWDkWsrD6fFQhQ9dZLfVbC5M88CWCPERr+8fLZodJ5M8QJbjb' \
           'GL1H2M1fIGfEm+wJN+bGCSc6EXtNS/8FSrq2VX6YDv++XLpJ8SgDWMnwqznGo6alcTbIxB2CHKn8VFikk2mMV2lEnV+CJd9+jJlxXmMr5' \
           'dW14YCqwgbFpO8FNvJxwwM4TPWPo5QalEsRMAcusXpi58/QUEWPL0AK1ThM5oQCUyXPoPINkdd922VBw4XgTV9zDGWWFrgjIQs4vwvOg6' \
           'xr+6gbCTqE+DYhlMGX0CF2OknK5gQ2JrkDh/W6TOEbYDeVecKbJtyNXiCfGmW7V93J2hDus1bDfhxWbIZVYDXITA7Lo6E0Ktgg9eB4KWu' \
           'R44aj7ppBVPazhQH7/M/KgWe9X1qAg8XypT6nxIMJH+T94QCsLvj29IYwZxyO9/F8vCbO9tX5/wDGjEZ7vrgFZwAAAABJRU5ErkJggg=='

    if helper.is_running_on_lambda():
        data_b64 = {
            'headers': headers,
            'statusCode': 200,
            'body': data,
            'isBase64Encoded': True
        }
        data = helper.to_json(data_b64)
        headers = {"Content-Type": "application/json"}
    else:
        data = base64.b64decode(data)

    return http_helper.create_response(body=data, status_code=200, headers=headers)


@APP.route(API_ROOT + '/favicon-16x16.png')
def favicon16():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "image/png"
    data = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAABNVBMVEVisTRhsTReqzVbpTVXoDdVnTdSlzh' \
           'RljgvXkAuXUAtWkErV0EzZj40Zj85bz0lTkMkTUMkT0MmTUIkS0IjTEIhSUMkS0IkTEIkTUIlTUIkTkMlTkMcQUQcP0UfQ0QdQ0QfREQg' \
           'RUMiSUMiSUMjSkInU0EkTEMmUEEiR0IiSEMpVkErWT8kTUElTUIUNkYVNEQVMkcRM0QSNUYQMUIMMUkVK0AAJEkAM00AMzMAAAAAAACF6' \
           'i2E6SyD6CyC5i2B5Sx/4i6A4S593S583S520jB00DByyjFxyTFwyDFvxjJtxTFtxDFswzJrwDJqvzJpvjNouzNoujNnuDNLjTlKijpKiT' \
           'pEfztDfzxAeT0+dz05bj44bT44bj82aj81aD8zZT8bPUUbPkUcP0UcPUUeQ0UfREQgRkRgJREvAAAAO3RSTlP09PX19vX39u7u7/Dq6uf' \
           'h4eDg4+Pf3Nvb2tnY2NvPv7y6rKupqaGZlpSOiYWETDEkHh0fFQwHCgUBAAcHrskAAADYSURBVHjaPc/ZLkNRGIbhz26KjVJpqSKGtjHP' \
           'c9a7W7OEEhtBjDWUO3XghqQSwVrNTp+j///OXhlrLpdJdg9MLblbxqwPd5RLUDpOjK66YWMwTqRpaM0OhZbo3dskljea9+HyAevxHtoWV' \
           'AjhfQtr5w3CSfUE8BrgvEDQpxRc3eyfH5wenlQuIO39Sb9x/8uv+bXvmPSjbABPRZznIkGvxkOo7mJtV+FsQsutcFvBuruG9kWZMY+G5p' \
           'zxlMp/KPKZSUs2cLrzyMWVEyP1OGtlNpvs6p+p5/8DzUo5hMDku9EAAAAASUVORK5CYII='

    if helper.is_running_on_lambda():
        data_b64 = {
            'headers': headers,
            'statusCode': 200,
            'body': data,
            'isBase64Encoded': True
        }
        data = helper.to_json(data_b64)
        headers = {"Content-Type": "application/json"}
    else:
        data = base64.b64decode(data)

    return http_helper.create_response(body=data, status_code=200, headers=headers)


@APP.route(API_ROOT + '/docs')
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/html"
    html_file = open_vendor_file('./public/swagger/index.html', 'r')
    html = html_file.read()
    return http_helper.create_response(
        body=html, status_code=200, headers=headers)


@APP.route(API_ROOT + '/openapi.yml')
def openapi():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/yaml"
    html_file = open_vendor_file('./public/swagger/openapi.yml', 'r')
    html = html_file.read()
    return http_helper.create_response(
        body=html, status_code=200, headers=headers)


# product routes
@APP.route(API_ROOT + '/v1/product', methods=['GET'])
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
                            schema: HateosProductListResponseSchema
                4xx:
                    description: Error response
                    content:
                        application/json:
                            schema: ProductListErrorResponseSchema
                5xx:
                    description: Service fail response
                    content:
                        application/json:
                            schema: ProductListErrorResponseSchema
        """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('request: {}'.format(request))

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(True)

    manager = ProductManager(logger=LOGGER, product_service=ProductServiceV1(logger=LOGGER))
    manager.debug(DEBUG)
    try:
        data = manager.list(request.to_dict())
        response.set_data(data)
        response.set_total(manager.count(request.to_dict()))

        # hateos
        response.links = None
        set_hateos_meta(request, response)
        # LOGGER.info(data)
        # LOGGER.info(response.data)
    except Exception as err:
        LOGGER.error(err)
        error = ApiException(MessagesEnum.LIST_ERROR)
        status_code = 400
        if manager.exception:
            error = manager.exception
        response.set_exception(error)

    return response.get_response(status_code)


@APP.route(API_ROOT + '/v1/product/<uuid>', methods=['GET'])
def product_get(uuid):
    """
        ---
        get:
            summary: Product Get
            parameters:
            - in: path
              name: uuid
              description: "Product Id"
              required: true
              schema:
                type: string
                format: uuid
                example: 4bcad46b-6978-488f-8153-1c49f8a45244
            - name: fields
              in: query
              description: "Filter fields with comma"
              required: false
              schema:
                type: string
                example:
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: HateosProductGetResponseSchema
                4xx:
                    description: Error response
                    content:
                        application/json:
                            schema: ProductGetErrorResponseSchema
                5xx:
                    description: Service fail response
                    content:
                        application/json:
                            schema: ProductGetErrorResponseSchema
    """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('request: {}'.format(request))

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(True)

    manager = ProductManager(logger=LOGGER, product_service=ProductServiceV1(logger=LOGGER))
    manager.debug(DEBUG)
    try:
        response.set_data(manager.get(request.to_dict(), uuid))

        # hateos
        set_hateos_links(request, response, uuid)
        set_hateos_meta(request, response, uuid)

    except Exception as error:
        LOGGER.error(error)
        if not isinstance(error, ValidationException):
            error = ApiException(MessagesEnum.FIND_ERROR)
        status_code = 400
        if manager.exception:
            error = manager.exception
        response.set_exception(error)

    return response.get_response(status_code)


@APP.route(API_ROOT + '/v1/product', methods=['POST'])
def product_create():
    """
        :return:
        ---
        post:
            summary: Product Create
            requestBody:
                description: 'Product to be created'
                required: true
                content:
                    application/json:
                        schema: ProductCreateRequestSchema
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: ProductCreateResponseSchema
                4xx:
                    description: Error response
                    content:
                        application/json:
                            schema: ProductCreateErrorResponseSchema
                5xx:
                    description: Service fail response
                    content:
                        application/json:
                            schema: ProductCreateErrorResponseSchema
            """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('request: {}'.format(request))

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(False)

    manager = ProductManager(logger=LOGGER, product_service=ProductServiceV1(logger=LOGGER))
    manager.debug(DEBUG)
    try:
        response.set_data(manager.create(request.to_dict()))
        # response.set_total(manager.count(request))

        # hateos
        # set_hateos_links(request, response, uuid)
        # set_hateos_meta(request, response, uuid)
    except Exception as error:
        LOGGER.error(error)
        if not isinstance(error, ValidationException):
            error = ApiException(MessagesEnum.CREATE_ERROR)
        status_code = 400
        if manager.exception:
            error = manager.exception
        response.set_exception(error)

    return response.get_response(status_code)


@APP.route('/v1/product/<uuid>', methods=['PUT'])
def product_update(uuid):
    """
        :return:
        ---
        put:
            summary: Complete Product Update
            parameters:
            - in: path
              name: uuid
              description: "Product Id"
              required: true
              schema:
                type: string
                format: uuid
                example: 4bcad46b-6978-488f-8153-1c49f8a45244
            requestBody:
                description: 'Product to be updated'
                required: true
                content:
                    application/json:
                        schema: ProductCompleteUpdateRequestSchema
            responses:
                200:
                    content:
                        application/json:
                            schema: ProductUpdateResponseSchema
                4xx:
                    description: Error response
                    content:
                        application/json:
                            schema: ProductUpdateErrorResponseSchema
                5xx:
                    description: Service fail response
                    content:
                        application/json:
                            schema: ProductUpdateErrorResponseSchema
            """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('request: {}'.format(request))

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(False)

    manager = ProductManager(logger=LOGGER, product_service=ProductServiceV1(logger=LOGGER))
    manager.debug(DEBUG)
    try:

        response.set_data(manager.update(request.to_dict(), uuid))
        # response.set_total(manager.count(request))
    except Exception as error:
        LOGGER.error(error)
        if not isinstance(error, ValidationException):
            error = ApiException(MessagesEnum.UPDATE_ERROR)
        status_code = 400
        if manager.exception:
            error = manager.exception
        response.set_exception(error)

    return response.get_response(status_code)


@APP.route('/v1/product/<uuid>', methods=['DELETE'])
def product_delete(uuid):
    """
            :return:
            ---
            delete:
                summary: Soft Product Delete
                parameters:
                - in: path
                  name: uuid
                  description: "Product Id"
                  required: true
                  schema:
                    type: string
                    format: uuid
                    example: 4bcad46b-6978-488f-8153-1c49f8a45244
                responses:
                    200:
                        description: Success response
                        content:
                            application/json:
                                schema: ProductSoftDeleteResponseSchema
                    4xx:
                        description: Error response
                        content:
                            application/json:
                                schema: ProductSoftDeleteErrorResponseSchema
                    5xx:
                        description: Service fail response
                        content:
                            application/json:
                                schema: ProductSoftDeleteErrorResponseSchema
                    """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('request: {}'.format(request))

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(False)

    manager = ProductManager(logger=LOGGER, product_service=ProductServiceV1(logger=LOGGER))
    manager.debug(DEBUG)
    try:
        data = {"deleted": manager.delete(request.to_dict(), uuid)}
        response.set_data(data)
        # response.set_total(manager.count(request))
    except Exception as error:
        LOGGER.error(error)
        if not isinstance(error, ValidationException):
            error = ApiException(MessagesEnum.DELETE_ERROR)
        status_code = 400
        if manager.exception:
            error = manager.exception
        response.set_exception(error)

    return response.get_response(status_code)


@APP.route('/v1/product/<uuid>', methods=['PATCH'])
def product_soft_update(uuid):
    """
        :return:
        ---
        patch:
            summary: Soft Product Update
            parameters:
            - in: path
              name: uuid
              description: "Product Id"
              required: true
              schema:
                type: string
                format: uuid
                example: 4bcad46b-6978-488f-8153-1c49f8a45244
            requestBody:
                description: 'Product field to be updated'
                required: true
                content:
                    application/json:
                        schema: ProductSoftUpdateRequestSchema

            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: ProductUpdateResponseSchema
                4xx:
                    description: Error response
                    content:
                        application/json:
                            schema: ProductUpdateErrorResponseSchema
                5xx:
                    description: Service fail response
                    content:
                        application/json:
                            schema: ProductUpdateErrorResponseSchema
                """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('request: {}'.format(request))

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(False)

    manager = ProductManager(logger=LOGGER, product_service=ProductServiceV1(logger=LOGGER))
    manager.debug(DEBUG)
    try:

        response.set_data(manager.soft_update(request.to_dict(), uuid))
        # response.set_total(manager.count(request))
    except Exception as error:
        LOGGER.error(error)
        if not isinstance(error, ValidationException):
            error = ApiException(MessagesEnum.UPDATE_ERROR)
        status_code = 400
        if manager.exception:
            error = manager.exception
        response.set_exception(error)

    return response.get_response(status_code)


@APP.route('/v1/event/<event_type>', methods=['POST'])
def event_create(event_type):
    """
    :param event_type:
    :return:
    ---
    post:
        summary: Create event
        parameters:
            - in: path
              name: event_type
              description: "Event type"
              required: true
              schema:
                type: string
                example: ocoren-event
        requestBody:
            description: 'Event to be created'
            required: true
            content:
                application/json:
                    schema: EventCreateRequest
        responses:
            200:
                content:
                    application/json:
                        schema: EventCreateResponseSchema
            4xx:
                content:
                    application/json:
                        schema: EventCreateErrorResponseSchema
        """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('event_type: {}'.format(event_type))
    LOGGER.info('request: {}'.format(request))

    event_tracker = EventTracker(LOGGER)

    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(False)
    try:
        # event_type validation
        if EventType.from_value(
                event_type) not in EventType.get_public_events():
            exception = ApiException(MessagesEnum.EVENT_TYPE_UNKNOWN_ERROR)
            exception.set_message_params([event_type])
            raise exception

        event_vo = EventVO(event_type=event_type, data=request.where)
        # if EventType.from_value(event_type) == EventType.OCOREN_EVENT:
        #     event_service = OcorenEventService()
        # else:
        #     event_service = ProductEventService()
        event_service = OcorenEventService()
        service = EventManager(logger=LOGGER, event_service=event_service)
        result = service.process(event_vo)
        event_hash = event_vo.hash

        event_tracker.track(event_hash, event_vo.to_dict())

        if result:
            code = MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.code
            label = MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.label
            message = MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.message
            params = None
        else:
            if isinstance(service.exception, ApiException):
                raise service.exception
            else:
                raise ApiException(MessagesEnum.INTERNAL_SERVER_ERROR)
    except Exception as err:
        LOGGER.error(err)
        result = False
        event_hash = None
        if isinstance(err, ApiException):
            api_ex = err
            status_code = 400
        else:
            api_ex = ApiException(MessagesEnum.CREATE_ERROR)
            status_code = 500

        code = api_ex.code
        label = api_ex.label
        message = api_ex.message
        params = api_ex.params

    data = {
        "result": result,
        "event_hash": event_hash,
        "code": code,
        "label": label,
        "message": message,
        "params": params
    }

    response.set_data(data)

    event_tracker.track(event_hash, data)
    return response.get_response(status_code)

# *************
# doc
# *************
spec.path(view=alive, path=API_ROOT + "/alive", operations=get_doc(alive))
# *************
# product
# *************
spec.path(view=product_list,
          path="/v1/product", operations=get_doc(product_list))
spec.path(view=product_get,
          path="/v1/product/{uuid}", operations=get_doc(product_get))
spec.path(view=product_create,
          path="/v1/product", operations=get_doc(product_create))
spec.path(view=product_update,
          path="/v1/product/{uuid}", operations=get_doc(product_update))
spec.path(view=product_soft_update,
          path="/v1/product/{uuid}", operations=get_doc(product_soft_update))
spec.path(view=product_delete,
          path="/v1/product/{uuid}", operations=get_doc(product_delete))
spec.path(view=event_create,
          path="/v1/event/{event_type}", operations=get_doc(event_create))
print_routes(APP, LOGGER)
LOGGER.info('Running at {}'.format(ENV))

# *************
# generate de openapi.yml
# *************
generate_openapi_yml(spec, LOGGER, force=True)

api_schemas.register()
