"""
Flambda Framework Decorator Module - Chalice Compatible
Version: 1.0.0
"""
from typing import Optional

from flambda_app.decorators.events import SQSEvent, SNSEvent, CloudWatchEvent, S3Event, \
    KinesisEvent, DynamoDBEvent, LambdaFunctionEvent
from flambda_app.decorators.wrappers import PureLambdaWrapper, SQSLambdaWrapper, EventSourceHandler, \
    ScheduleLambdaWrapper

_EVENT_CLASSES = {
    'on_s3_event': S3Event,
    'on_sns_message': SNSEvent,
    'on_sqs_message': SQSEvent,
    'on_cw_event': CloudWatchEvent,
    'on_kinesis_record': KinesisEvent,
    'on_dynamodb_record': DynamoDBEvent,
    'schedule': CloudWatchEvent,
    'lambda_function': LambdaFunctionEvent
}


def _wrap_handler(handler_type, handler_name, user_handler):
    if handler_type == 'lambda_function':
        user_handler = PureLambdaWrapper(user_handler)
    elif handler_type == 'on_sqs_message':
        user_handler = SQSLambdaWrapper(user_handler)
    elif handler_type == 'schedule':
        user_handler = ScheduleLambdaWrapper(user_handler)
    return EventSourceHandler(
        user_handler, _EVENT_CLASSES[handler_type],
        middleware_handlers=None
    )

    # if handler_type in _EVENT_CLASSES:
    #     if handler_type == 'lambda_function':
    #         # We have to wrap existing @app.lambda_function()
    #         # handlers for backwards compat reasons so we can
    #         # preserve the `def handler(event, context): ...`
    #         # interface.  However we need a consistent interface
    #         # for middleware so we have to wrap the event
    #         # here.
    #         user_handler = PureLambdaWrapper(user_handler)
    #     return EventSourceHandler(
    #         user_handler, _EVENT_CLASSES[handler_type],
    #         middleware_handlers=self._get_middleware_handlers(
    #             event_type=_MIDDLEWARE_MAPPING[handler_type],
    #         )
    #     )
    #
    # websocket_event_classes = [
    #     'on_ws_connect',
    #     'on_ws_message',
    #     'on_ws_disconnect',
    # ]
    # if handler_type in websocket_event_classes:
    #     return WebsocketEventSourceHandler(
    #         user_handler, WebsocketEvent,
    #         self.websocket_api,  # pylint: disable=no-member
    #         middleware_handlers=self._get_middleware_handlers(
    #             event_type='websocket')
    #     )
    # if handler_type == 'authorizer':
    #     # Authorizer is special cased and doesn't quite fit the
    #     # EventSourceHandler pattern.
    #     return ChaliceAuthorizer(handler_name, user_handler)
    # return user_handler


class LambdaDecorator:

    def on_s3_event(self, bucket: str, events= None,
                    prefix: Optional[str] = None, suffix: Optional[str] = None,
                    name: Optional[str] = None):
        return self._create_registration_function(
            handler_type='on_s3_event',
            name=name,
            registration_kwargs={
                'bucket': bucket, 'events': events,
                'prefix': prefix, 'suffix': suffix,
            }
        )

    def on_sns_message(self, topic: str,
                       name: Optional[str] = None):
        return self._create_registration_function(
            handler_type='on_sns_message',
            name=name,
            registration_kwargs={'topic': topic}
        )

    def on_sqs_message(self, queue, batch_size=1, name=None):
        return self._create_registration_function(
            handler_type='on_sqs_message',
            name=name,
            registration_kwargs={'queue': queue, 'batch_size': batch_size}
        )

    def schedule(self, expression,
                 name=None,
                 description: str = ''):
        return self._create_registration_function(
            handler_type='schedule',
            name=name,
            registration_kwargs={'expression': expression,
                                 'description': description},
        )

    def _create_registration_function(self, handler_type, name=None,
                                      registration_kwargs=None):
        def _register_handler(user_handler):
            handler_name = name
            if handler_name is None:
                handler_name = user_handler.__name__
            if registration_kwargs is not None:
                kwargs = registration_kwargs
            else:
                kwargs = {}
            wrapped = _wrap_handler(handler_type, handler_name,
                                    user_handler)
            self._register_handler(handler_type, handler_name,
                                   user_handler, wrapped, kwargs)
            return wrapped

        return _register_handler

    def _register_handler(self, handler_type, name,
                          user_handler, wrapped_handler, kwargs, options=None):
        # TODO info: This project dont register actions to be executed like chalice (Terra formation)

        # raise NotImplementedError("_register_handler")
        # self.logger.info("_register_handler")
        pass

    # def _register_schedule(self, name: str, handler_string: str,
    #                        kwargs: Any, **unused: Dict[str, Any]) -> None:
    # TODO info: This project dont register actions to be executed like chalice (Terra formation)
    #     event_source = ScheduledEventConfig(
    #         name=name,
    #         schedule_expression=kwargs['expression'],
    #         description=kwargs["description"],
    #         handler_string=handler_string,
    #     )
    #     self.event_sources.append(event_source)
