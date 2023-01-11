"""
Request Control Module for Flambda APP
Version: 1.0.0
"""
from flambda_app import constants


class PaginationType:
    LIMIT = 'limit'
    OFFSET = 'offset'


class Pagination:
    """
    """
    LIMIT = constants.LIMIT
    OFFSET = constants.OFFSET

    @staticmethod
    def validate(pagination_type, value):
        """
        :param pagination_type:
        :param value:
        :return:
        """
        try:
            if str(pagination_type).lower() == PaginationType.LIMIT:
                if int(value) > constants.PAGINATION_LIMIT:
                    value = constants.PAGINATION_LIMIT
                elif int(value) < 0:
                    value = Pagination.OFFSET
            else:
                if int(value) < 0:
                    value = Pagination.OFFSET
        except Exception as err:
            if str(pagination_type).lower() == PaginationType.LIMIT:
                value = Pagination.LIMIT
            else:
                value = Pagination.OFFSET
        return int(value)


class Order:
    ASC = 'ASC'
    DESC = 'DESC'

    @staticmethod
    def validate(value):
        if value != Order.ASC:
            value = Order.DESC
        return value
