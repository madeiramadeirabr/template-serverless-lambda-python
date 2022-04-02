import uuid

from flambda_app.helper import datetime_now_with_timezone
from flambda_app.vos import AbstractVO


class ProductVO(AbstractVO):
    def __init__(self, data:dict = None):
        self.id = data.get('id') if data and "id" in data else None
        self.uuid = data.get('uuid') if data and "uuid" in data else str(uuid.uuid4())
        self.sku = data.get('sku') if data and "sku" in data else None
        self.name = data.get('name') if data and "name" in data else None
        self.description = data.get('description') if data and 'description' in data else None
        self.supplier_id = data.get('supplier_id') if data and 'supplier_id' in data else None
        self.created_at = data.get('created_at') if data and 'created_at' in data else datetime_now_with_timezone().isoformat()
        self.updated_at = data.get('updated_at') if data and 'updated_at' in data else None
        self.deleted_at = data.get('deleted_at') if data and 'deleted_at' in data else None
