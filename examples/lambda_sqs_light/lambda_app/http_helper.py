from flask import Response
from flask import jsonify
from lambda_app import APP_VERSION, APP_ARCH_VERSION, helper

# Conflito interno
# ModuleNotFoundError: No module named 'http.client'; 'http' is not a package

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

