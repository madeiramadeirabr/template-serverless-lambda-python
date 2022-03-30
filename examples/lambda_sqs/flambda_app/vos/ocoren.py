"""
Ocoren Value Object Module for Flambda APP
Version: 1.0.0
"""
from flambda_app import helper
from flambda_app.helper import datetime_now_with_timezone
from flambda_app.vos import AbstractVO


class OcorenVO(AbstractVO):
    def __init__(self, data:dict = None):
        self.id = data.get('id') if data and "id" in data else None
        self.chavenfe = data.get('chavenfe') if data and "chavenfe" in data else None
        self.ocor = data.get('ocor') if data and "ocor" in data else None
        self.origem = data.get('origem') if data and "origem" in data else None
        self.pedido = data.get('pedido') if data and 'pedido' in data else None
        self.created_at = data.get('created_at') if data and 'created_at' in data else \
            helper.datetime_format_for_database(datetime_now_with_timezone())
        self.updated_at = data.get('updated_at') if data and 'updated_at' in data else None
        self.deleted_at = data.get('deleted_at') if data and 'deleted_at' in data else None
