from lambda_app import helper
from lambda_app.helper import datetime_now_with_timezone, generate_hash
from lambda_app.vos import AbstractVO


class EventVO(AbstractVO):
    def __init__(self, event_type, data:dict):
        """
        :param event_type:
        :param dict data:
        """
        self.type = event_type
        self.data = data
        self.date = helper.datetime_format_for_database(datetime_now_with_timezone())
        self.hash = generate_hash(self.data)