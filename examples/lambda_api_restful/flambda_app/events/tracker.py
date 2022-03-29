"""
Event Tracker Module for Flambda APP
Version: 1.0.0
"""
from flambda_app.logging import get_logger


class EventTracker:
    def __init__(self, logger=None):
        """
        # This cant import get_config
        :param logger:
        """
        # logger
        self.logger = logger if logger is not None else get_logger()
        # last_exception
        self.exception = None

    def track(self, event_hash, event_data):
        self.logger.info('Track event: {} - {}'.format(event_hash, event_data))

    def track_error(self, event_hash, event_data, exception):
        self.logger.error('Track event: {} - {} - {}'.format(event_hash, event_data, exception))
