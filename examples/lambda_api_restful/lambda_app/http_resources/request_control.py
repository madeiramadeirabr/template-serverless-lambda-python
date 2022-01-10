class PaginationType:
    LIMIT = 'limit'
    OFFSET = 'offset'


PAGINATION_LIMIT = 100


class Pagination:
    """
    """
    LIMIT = 20
    OFFSET = 0

    @staticmethod
    def validate(pagination_type, value):
        """
        :param pagination_type:
        :param value:
        :return:
        """
        try:
            if str(pagination_type).lower() == PaginationType.LIMIT:
                if int(value) > PAGINATION_LIMIT:
                    value = PAGINATION_LIMIT
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