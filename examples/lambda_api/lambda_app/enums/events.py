
from lambda_app.enums import CustomStringEnum


class EventType(CustomStringEnum):
    UNKNOWN = 'unknown'
    OCOREN_EVENT = 'ocoren-event'

    @classmethod
    def get_public_events(cls):
        return [cls.OCOREN_EVENT]