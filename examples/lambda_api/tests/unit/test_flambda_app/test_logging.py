import logging
import unittest

from flambda_app.logging import get_logger, reset as reset_logger, LoggerProfile, remove_handler
from tests.unit.testutils import BaseUnitTestCase, get_function_name
from unittest_data_provider import data_provider


def get_profiles():
    return (None,), (LoggerProfile.CONSOLE,), (LoggerProfile.NEWRELIC,), (LoggerProfile.ELK,)


class LoggingTestCase(BaseUnitTestCase):

    @data_provider(get_profiles)
    def test_logger_by_profiles(self, profile):
        self.logger.info('Running test: %s', get_function_name(__name__))
        reset_logger()
        event = {"event_name": "TEST"}

        # TODO mockar o es client
        logger = get_logger(profile)

        logger.info("something", extra=event)
        logger.error("something 2", extra=event)

    def test_logger_kwargs(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        profile = LoggerProfile.ELK
        reset_logger()
        event = {"event_name": "TEST"}

        # TODO mockar o es client
        logger = get_logger(profile, default_index='logs')

        logger.info("something", extra=event)
        logger.error("something 2", extra=event)

    def test_remove_handler(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        profile = LoggerProfile.ELK
        logger = get_logger(profile, default_index='logs')
        logger.addHandler(logging.StreamHandler())
        remove_handler(logger, logging.StreamHandler)


if __name__ == '__main__':
    unittest.main()
