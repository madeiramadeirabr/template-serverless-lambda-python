from lambda_app import helper
from lambda_app.decorators.events import SQSRecord, SQSEvent


class EventSourceHandler:
    def __init__(self, func, event_class, middleware_handlers=None):
        self.func = func
        self.event_class = event_class
        if middleware_handlers is None:
            middleware_handlers = []
        self._middleware_handlers = middleware_handlers
        self.handler = None

    def __call__(self, event, context):
        event_obj = self.event_class(event, context)

        # if self.handler is None:
        #     # Defer creating handlers so we have all middleware configured.
        #     self.handler = self._build_middleware_handlers(
        #         self._middleware_handlers, original_handler=self.func)
        # return self.handler(event_obj)
        return self.func(event_obj)


class PureLambdaWrapper(object):
    def __init__(self, original_func):
        self._original_func = original_func

    def __call__(self, event):
        # The @app.lambda_function() expects an event dict
        # and a context argument so this class will is used to adapt
        # from the Chalice single-arg style function (which is used
        # in all the event handlers) to the low-level lambda api.
        return self._original_func(event.to_dict(), event.context)


class SQSLambdaWrapper(object):
    def __init__(self, original_func):
        self._original_func = original_func

    def __call__(self, event):
        if isinstance(event, SQSEvent) or isinstance(event, SQSRecord):
            record = event
        else:
            if helper.has_attr(event, 'body'):
                record = SQSRecord(helper.to_dict(event), event.context)
            else:
                record = SQSEvent(helper.to_dict(event), event.context)
        return self._original_func(record)
