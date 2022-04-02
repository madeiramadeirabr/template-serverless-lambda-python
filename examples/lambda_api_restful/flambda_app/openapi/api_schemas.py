"""
API Schemas Module for Flambda APP
Version: 1.0.0
"""
from marshmallow import Schema, fields, validate

from flambda_app.enums.messages import MessagesEnum
from flambda_app.openapi.schemas import DeletionSchema, RequestControlSchema, MetaSchema, LinkSchema, ErrorSchema, \
    HateosDefaultListResponseSchema, DefaultResponseSchema, HateosDefaultResponseSchema


# ***************************
# Product
# ***************************
class ProductSchema(Schema):
    id = fields.Int(example=1)
    sku = fields.Int(example=657705)
    name = fields.Str(example="Guarda Roupa Casal com Espelho 3 Portas de Correr Lara Espresso Móveis")
    description = fields.Str(example="Guarda Roupa com maior resistência, durabilidade e acabamento, revestimento "
                                     "interno e externo. Pintura em estufas modernas com UV (ultra violeta). "
                                     "Modelo com corrediça metálica em aço, 4 gavetas espaçosas, perfil em alumínio, "
                                     "roldanas de aço carbono com rolamento, divisão ele/ela")
    supplier_id = fields.Int(example=1)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    deleted_at = fields.DateTime()
    active = fields.Int(validate=validate.OneOf([0, 1]))
    uuid = fields.UUID(example="4bcad46b-6978-488f-8153-1c49f8a45244")


class HateosProductListResponseSchema(HateosDefaultListResponseSchema):
    data = fields.List(fields.Nested(ProductSchema))
    control = fields.Nested(RequestControlSchema)


class ProductListResponseSchema(DefaultResponseSchema):
    data = fields.List(fields.Nested(ProductSchema))
    control = fields.Nested(RequestControlSchema)


class ProductListErrorResponseSchema(ErrorSchema):
    code = fields.Int(example=MessagesEnum.LIST_ERROR.code, required=True)
    label = fields.Str(example=MessagesEnum.LIST_ERROR.label)
    message = fields.Str(example=MessagesEnum.LIST_ERROR.message)


class ProductGetResponseSchema(DefaultResponseSchema):
    data = fields.Nested(ProductSchema)


class HateosProductGetResponseSchema(HateosDefaultResponseSchema):
    data = fields.Nested(ProductSchema)


class ProductGetErrorResponseSchema(ErrorSchema):
    code = fields.Int(example=MessagesEnum.FIND_ERROR.code, required=True)
    label = fields.Str(example=MessagesEnum.FIND_ERROR.label)
    message = fields.Str(example=MessagesEnum.FIND_ERROR.message)


class ProductCreateRequestSchema(Schema):
    sku = fields.Int(example=657705)
    name = fields.Str(example="Guarda Roupa Casal com Espelho 3 Portas de Correr Lara Espresso Móveis")
    description = fields.Str(example="Guarda Roupa com maior resistência, durabilidade e acabamento, revestimento "
                                     "interno e externo. Pintura em estufas modernas com UV (ultra violeta). "
                                     "Modelo com corrediça metálica em aço, 4 gavetas espaçosas, perfil em alumínio, "
                                     "roldanas de aço carbono com rolamento, divisão ele/ela")
    supplier_id = fields.Int(example=1)
    active = fields.Int(validate=validate.OneOf([0, 1]))


class ProductCreateResponseSchema(DefaultResponseSchema):
    data = fields.Nested(ProductSchema)


class ProductCreateErrorResponseSchema(ErrorSchema):
    code = fields.Int(example=MessagesEnum.CREATE_ERROR.code, required=True)
    label = fields.Str(example=MessagesEnum.CREATE_ERROR.label)
    message = fields.Str(example=MessagesEnum.CREATE_ERROR.message)


class ProductCompleteUpdateRequestSchema(ProductCreateRequestSchema):
    pass


class ProductUpdateResponseSchema(ProductCreateResponseSchema):
    pass


class ProductUpdateErrorResponseSchema(ErrorSchema):
    code = fields.Int(example=MessagesEnum.UPDATE_ERROR.code, required=True)
    label = fields.Str(example=MessagesEnum.UPDATE_ERROR.label)
    message = fields.Str(example=MessagesEnum.UPDATE_ERROR.message)


class ProductSoftUpdateRequestSchema(Schema):
    field = fields.Str(example="value")


class ProductSoftDeleteResponseSchema(DefaultResponseSchema):
    data = fields.Dict(example={"deleted": True})


class ProductDeleteResponseSchema(Schema):
    data = fields.Dict(example={"deleted": True})


class ProductSoftDeleteErrorResponseSchema(ErrorSchema):
    code = fields.Int(example=MessagesEnum.SOFT_DELETE_ERROR.code, required=True)
    label = fields.Str(example=MessagesEnum.SOFT_DELETE_ERROR.label)
    message = fields.Str(example=MessagesEnum.SOFT_DELETE_ERROR.message)


class ProductDeleteErrorResponseSchema(ErrorSchema):
    code = fields.Int(example=MessagesEnum.DELETE_ERROR.code, required=True)
    label = fields.Str(example=MessagesEnum.DELETE_ERROR.label)
    message = fields.Str(example=MessagesEnum.DELETE_ERROR.message)

# ***************************
# Event
# ***************************


class EventSchema(Schema):
    type = fields.Str()
    data = fields.Dict()
    date = fields.DateTime(example="2021-05-03T19:41:36.315842-03:00")
    hash = fields.Str(example="406cce9743906f7b8d7dd5d5c5d8c95d820eeefd72a3a554a4a726d022d8fa19")


class OcorenSchema(Schema):
    chavenfe = fields.Str(example="32210206107255000134550010001712551245826554")
    ocor = fields.Str(example="MOTIVO DO CANCELAMENTO")
    origem = fields.Str(example="SAC/EAGLE")
    pedido = fields.Str(example="Z1223321")


class EventCreateRequestSchema(OcorenSchema):
    pass


class EventUpdateRequestSchema(EventCreateRequestSchema):
    pass


class EventListResponseSchema(DefaultResponseSchema):
    data = fields.List(fields.Nested(EventSchema))
    control = fields.Nested(RequestControlSchema)
    meta = fields.Nested(MetaSchema)
    links = fields.List(fields.Nested(LinkSchema))


class EventListErrorResponseSchema(ErrorSchema):
    pass


class EventGetResponseSchema(Schema):
    data = fields.Nested(EventSchema)
    control = fields.Nested(RequestControlSchema)
    meta = fields.Nested(MetaSchema)
    links = fields.List(fields.Nested(LinkSchema))


class EventCreateResponseSchema(Schema):
    result = fields.Bool(example=True)
    event_hash = fields.Str(example="c82bf3ee20dd2f4ae7109e52d313a3190f1a85ba3362c54d3eb6257bd0c4d69d")
    code = fields.Int(example=MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.code)
    label = fields.String(example=MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.label)
    message = fields.String(example=MessagesEnum.EVENT_REGISTERED_WITH_SUCCESS.message)
    params = fields.List(fields.Str())


class EventCreateErrorResponseSchema(Schema):
    result = fields.Bool(example=False)
    event_hash = fields.Str(example=None)
    code = fields.Int(example=MessagesEnum.EVENT_TYPE_UNKNOWN_ERROR.code)
    label = fields.String(example=MessagesEnum.EVENT_TYPE_UNKNOWN_ERROR.label)
    message = fields.String(example=MessagesEnum.EVENT_TYPE_UNKNOWN_ERROR.message)
    params = fields.List(fields.Str())


class EventUpdateResponseSchema(EventGetResponseSchema):
    pass


class EventDeleteResponseSchema(EventGetResponseSchema):
    data = fields.Nested(DeletionSchema)


def register():
    # simple function only to force the import of the script on app.py
    pass
