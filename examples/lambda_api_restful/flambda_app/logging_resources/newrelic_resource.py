"""
NewRelic Logging Resource SQS Based Module for Flambda APP
Version: 1.0.0
Import the logging module and the New Relic log formatter
https://docs.newrelic.com/docs/logs/logs-context/configure-logs-context-python/#python-formatter
"""
import atexit
import logging
import queue
import threading
import time
from threading import Timer

from newrelic.agent import NewRelicContextFormatter

from flambda_app import helper
from flambda_app.aws.sqs import SQS
from flambda_app.config import get_config
from flambda_app.logging import get_console_logger, get_log_level

_HANDLER_INSTANCE = None
_PAYLOAD_SIZE = 25
_SQS_INSTANCE = None
_LOGGER = None


def get_internal_logger():
    global _LOGGER
    if _LOGGER is None:
        logger = get_console_logger()
        logger.setLevel(get_log_level())
    else:
        logger = _LOGGER
    return logger


def set_sqs_instance(sqs_event):
    global _SQS_INSTANCE
    _SQS_INSTANCE = sqs_event if sqs_event is not None else SQS(logger=get_internal_logger())


def get_sqs_instance():
    """
    Singleton para SQS
    :return:
    """
    global _SQS_INSTANCE
    if _SQS_INSTANCE is None:
        _SQS_INSTANCE = SQS(logger=get_internal_logger())
        # faz o teste de conexão
        _SQS_INSTANCE.connect()
    return _SQS_INSTANCE


def divide_chunks(iterable, n=None):
    if n is None:
        n = _PAYLOAD_SIZE
    # looping till length l
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]


def final_newrelic_sqs_send_records():
    newrelic_sqs_send_records()


def stop():
    global _HANDLER_INSTANCE
    handler = _HANDLER_INSTANCE

    # encerra a execução do interval
    if handler.interval_handler is not None:
        handler.interval_handler.cancel()
        handler.interval_handler = None


def newrelic_sqs_send_records():
    global _HANDLER_INSTANCE

    # print('newrelic_sqs_send_records')
    if helper.debug_mode():
        get_internal_logger().info("executing newrelic_sqs_send_records")

    handler = _HANDLER_INSTANCE
    records = handler.get_records()

    config = get_config()

    queue_url = config.get('APP_LOGS_QUEUE', None)
    # so tenta enviar se for maior que zero
    if len(records) > 0:
        sqs = get_sqs_instance()

        try:
            response = sqs.send_message(records, queue_url)
            # print(response)
            if helper.debug_mode():
                get_internal_logger().info(response)

        except Exception as err:
            get_internal_logger().error(helper.to_json(err))


class SetInterval:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.stop_event = threading.Event()
        thread = threading.Thread(target=self.__set_interval)
        thread.start()

    def __set_interval(self):
        next_time = time.time() + self.interval
        while not self.stop_event.wait(next_time - time.time()):
            next_time += self.interval
            self.callback()

    def cancel(self):
        self.stop_event.set()


class NewRelicHandler(logging.Handler):
    MODE_THREADS = 'threads'
    MODE_INTERVAL = 'interval'

    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._error_queue = queue.Queue()
        # items per queue record
        self.payload_size = _PAYLOAD_SIZE
        # a cada 5 itens
        self.queue_send_size = 5
        self.thread_qty = 0
        self.thread_limit = 5
        self.mode = self.MODE_INTERVAL
        self.interval_handler = None
        # 300 ms
        self.interval_timer = 0.300

    def emit(self, record: logging.LogRecord):
        record_dict = record.__dict__
        # usa apenas uma unica fila
        self.put_record(record_dict)

        if self.mode == self.MODE_THREADS:
            raise NotImplementedError('Not implemented yet')
        else:
            # mode interval
            if self.interval_handler is None:
                # enquanto nao termina a execução  via timer, o interval vai se repetir por x vezes
                self.interval_handler = SetInterval(self.interval_timer, newrelic_sqs_send_records)
                t = Timer(2, stop)
                t.start()

    def put_record(self, record):
        self._queue.put(record)

    def get_records(self):
        records = []
        queue_size = self._queue.qsize()
        if queue_size > 0:
            for index in range(0, self.payload_size):
                if index < queue_size:
                    # para cada record
                    item = self._queue.get()
                    records.append(item)

        return records


class CustomNewRelicContextFormatter(NewRelicContextFormatter):
    def __init__(self, *args, **kwargs):
        super(CustomNewRelicContextFormatter, self).__init__()

    @classmethod
    def log_record_to_dict(cls, record):
        logging_default_attributes_keys = [
            'service', 'service_name', 'hostname', 'environment', 'entity.guid'
        ]
        logging_default_attributes = {}
        output = NewRelicContextFormatter.log_record_to_dict(record)

        for k in logging_default_attributes_keys:
            try:
                if hasattr(record, k):
                    logging_default_attributes[k] = getattr(record, k)
            except Exception as err:
                get_internal_logger().error(err)
                logging_default_attributes[k] = ""
        output.update(logging_default_attributes)

        return output


def get_formatter():
    return CustomNewRelicContextFormatter()


def get_handler():
    global _HANDLER_INSTANCE
    if _HANDLER_INSTANCE is None:
        # Instantiate a new log handler
        handler = NewRelicHandler()
        # Instantiate the log formatter and add it to the log handler
        handler.setFormatter(get_formatter())
        _HANDLER_INSTANCE = handler
    else:
        handler = _HANDLER_INSTANCE
    return handler


def add_newrelic_handler(logger, **kwargs):
    # newrelic
    try:
        handler = get_handler()
        # format in json for newrelic
        # handler.setFormatter(get_formatter())
        handler.setLevel(logger.level)
        # print("add_newrelic_handler > logger.level", logger.level)
        logger.addHandler(handler)

        # registra o envio final ao termino do script
        atexit.register(final_newrelic_sqs_send_records)

    except Exception as err:
        logger.error(err)
        logger.error("Newrelic not available")
