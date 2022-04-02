"""
NewRelic Logging Resource Module for Flambda APP
Version: 1.0.0
Import the logging module and the New Relic log formatter
https://docs.newrelic.com/docs/logs/logs-context/configure-logs-context-python/#python-formatter
"""
import logging

from newrelic.agent import NewRelicContextFormatter


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
            except Exception:
                logging_default_attributes[k] = ""
        output.update(logging_default_attributes)

        return output


def get_formatter():
    return CustomNewRelicContextFormatter()


def get_handler():
    # Instantiate a new log handler
    stream_handler = logging.StreamHandler()
    # Instantiate the log formatter and add it to the log handler
    formatter = get_formatter()
    stream_handler.setFormatter(formatter)
    return stream_handler


def add_newrelic_handler(logger, stream_handler=None, **kwargs):
    # newrelic
    try:
        if stream_handler is None:
            stream_handler = get_handler()
        # format in json for newrelic
        stream_handler.setFormatter(get_formatter())
        logger.info("Newrelic available")
    except Exception as err:
        logger.error(err)
        logger.info("Newrelic not available")
