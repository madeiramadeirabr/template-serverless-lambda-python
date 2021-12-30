"""This is the main file of the lambda application

This module contains the handler method
"""
import os
import base64
from lambda_app.services.v1.healthcheck import HealthCheckSchema
from lambda_app.services.v1.healthcheck.resources import \
    MysqlConnectionHealthCheck, RedisConnectionHealthCheck, \
    SQSConnectionHealthCheck, SelfConnectionHealthCheck
from lambda_app.services.v1.healthcheck_service import HealthCheckService
from lambda_app.config import get_config
from lambda_app.enums.events import EventType
from lambda_app.enums.messages import MessagesEnum
from lambda_app.events.tracker import EventTracker
from lambda_app.exceptions import ApiException
from lambda_app.http_resources.request import ApiRequest
from lambda_app.http_resources.response import ApiResponse
from lambda_app.services.v1.ocoren_event_service import OcorenEventService
from lambda_app.vos.events import EventVO
from lambda_app.logging import get_logger
from lambda_app import APP_NAME, APP_VERSION, http_helper
from lambda_app.helper import open_vendor_file, print_routes
from lambda_app.http_helper import CUSTOM_DEFAULT_HEADERS
from lambda_app.lambda_flask import LambdaFlask
from lambda_app.openapi import spec, get_doc, generate_openapi_yml
from lambda_app.openapi import api_schemas
from lambda_app.services.event_manager import EventManager
from lambda_app import helper
from lambda_app.boot import load_dot_env

# load env
ENV = helper.get_environment()
load_dot_env(ENV)


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


@APP.route('/v1/event/<event_type>', methods=['GET'])
def event_list(event_type):
    """
    :param event_type:
    :return:
    ---
    get:
        summary: List event
        parameters:
            - in: path
              name: event_type
              description: "Event type"
              required: true
              schema:
                type: string
                example: ocoren-event
        responses:
            200:
                content:
                    application/json:
                        schema: EventListResponseSchema
            4xx:
                content:
                    application/json:
                        schema: EventListErrorResponseSchema
        """
    request = ApiRequest().parse_request(APP)
    LOGGER.info('event_type: {}'.format(event_type))
    LOGGER.info('request: {}'.format(request))

    # event_tracker = EventTracker(logger)
    #
    status_code = 200
    response = ApiResponse(request)
    response.set_hateos(False)
    # try:
    #     # event_type validation
    #     if EventType.from_value(event_type) not in EventType.get_public_events():
    #         exception = ApiException(MessagesEnum.EVENT_TYPE_UNKNOWN_ERROR)
    #         exception.set_message_params([event_type])
    #         raise exception
    #
    #     event_vo = EventVO(event_type=event_type, data=request.where)
    #     # if EventType.from_value(event_type) == EventType.OCOREN_EVENT:
    #     #     event_service = OcorenEventService()
    #     # else:
    #     #     event_service = ProductEventService()
    #     event_service = OcorenEventService()
    #     service = EventManager(logger=logger, event_service=event_service)
    #     result = service.process(event_vo)
    #     event_hash = event_vo.hash
    #
    #     event_tracker.track(event_hash, event_vo.to_dict())
    #
    #     if result:
    #         code = MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.code
    #         label = MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.label
    #         message = MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.message
    #         params = None
    #     else:
    #         if isinstance(service.exception, ApiException):
    #             raise service.exception
    #         else:
    #             raise ApiException(MessagesEnum.INTERNAL_SERVER_ERROR)
    # except Exception as err:
    #     logger.error(err)
    #     result = False
    #     event_hash = None
    #     if isinstance(err, ApiException):
    #         api_ex = err
    #         status_code = 400
    #     else:
    #         api_ex = ApiException(MessagesEnum.CREATE_ERROR)
    #         status_code = 500
    #
    #     code = api_ex.code
    #     label = api_ex.label
    #     message = api_ex.message
    #     params = api_ex.params
    #
    # data = {
    #     "result": result,
    #     "event_hash": event_hash,
    #     "code": code,
    #     "label": label,
    #     "message": message,
    #     "params": params
    # }

    data = {}

    response.set_data(data)
    response.set_total(len(data))

    # event_tracker.track(event_hash, data)
    return response.get_response(status_code)


# doc
spec.path(view=alive, path="/alive", operations=get_doc(alive))
spec.path(view=event_list,
          path="/v1/event/{event_type}", operations=get_doc(event_list))
spec.path(view=event_create,
          path="/v1/event/{event_type}", operations=get_doc(event_create))

print_routes(APP, LOGGER)
LOGGER.info('Running at {}'.format(os.environ['APP_ENV']))

# generate de openapi.yml
generate_openapi_yml(spec, LOGGER, force=True)
