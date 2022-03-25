"""
HTTP Helper Module for Flambda APP
Version: 1.0.0
"""
from flask import Response
from flambda_app import APP_VERSION, APP_ARCH_VERSION, helper


# https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Controle_Acesso_CORS
# custom headers of the app
CUSTOM_DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Custom-Arch-Version': APP_ARCH_VERSION,
    'Custom-Service-Version': APP_VERSION,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS, GET, POST, PATH, PUT, DELETE',
    # 'Access-Control-Allow-Headers': 'Content-Type'
}


def validate_field(field, entity_fields):
    filtered = None
    if entity_fields and field in entity_fields:
        filtered = field
    return filtered


def validate_fields(fields, entity_fields):
    # print('fields', fields)
    # print(entity_fields)
    filtered = None
    if isinstance(fields, list):
        filtered = []
        for field in fields:
            validated = validate_field(field, entity_fields)
            if validated:
                filtered.append(validated)
    return filtered


def create_response(body=None, status_code=None, headers=None):
    if not headers:
        headers = CUSTOM_DEFAULT_HEADERS
    if isinstance(body, Exception):
        if helper.has_attr(body, 'STATUS_CODE'):
            status_code = body.STATUS_CODE
        else:
            status_code = 400
        return Response(response=str(body), status=status_code, headers=headers)
    else:
        if 'Content-Type' in headers and headers['Content-Type'] == 'application/json':
            body = helper.to_json(body)
        return Response(response=body, status=status_code, headers=headers)


def set_hateos_links(request, response, ref=None):
    try:
        from flambda_app.http_resources.hateos import HateosLink, HateosMeta
        current_url = request.protocol + request.host + request.path
        href = current_url.format(ref)
        response.set_hateos_link(HateosLink.UPDATE, href)
        response.set_hateos_link(HateosLink.DELETE, href)
        response.set_hateos_link(HateosLink.PATCH, href)
    except Exception as err:
        from flambda_app.logging import get_logger
        get_logger().error(err)


def set_hateos_meta(request, response, ref=None):
    try:
        from flambda_app.http_resources.hateos import HateosLink, HateosMeta
        current_url = request.protocol + request.host + request.path + '?' + request.query_string
        href = current_url.format(ref)
        response.set_meta(HateosMeta.HREF, href)
        response.set_meta(HateosMeta.NEXT, "")
        response.set_meta(HateosMeta.PREVIOUS, "")
        response.set_meta(HateosMeta.FIRST, "")
        response.set_meta(HateosMeta.LAST, "")
    except Exception as err:
        from flambda_app.logging import get_logger
        get_logger().error(err)
