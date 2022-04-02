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
        if 'Content-Type' in headers and headers['Content-Type']=='application/json':
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


def get_favicon_32x32_data():
    return 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAkFBMVEUAAAAQM0QWNUYWNkYXNkYALjoWNUYY' \
           'OEUXN0YaPEUPMUAUM0QVNUYWNkYWNUYWNUUWNUYVNEYWNkYWNUYWM0eF6i0XNkchR0OB5SwzZj9wyTEvXkA3' \
           'az5apTZ+4C5DgDt31C9frjU5bz5uxTI/eDxzzjAmT0IsWUEeQkVltzR62S6D6CxIhzpKijpJiDpOkDl4b43l' \
           'AAAAFXRSTlMAFc304QeZ/vj+ECB3xKlGilPXvS2Ka/h0AAABfklEQVR42oVT2XaCMBAdJRAi7pYJa2QHxbb/' \
           '/3ctSSAUPfa+THLmzj4DBvZpvyauS9b7kw3PWDkWsrD6fFQhQ9dZLfVbC5M88CWCPERr+8fLZodJ5M8QJbjb' \
           'GL1H2M1fIGfEm+wJN+bGCSc6EXtNS/8FSrq2VX6YDv++XLpJ8SgDWMnwqznGo6alcTbIxB2CHKn8VFikk2mM' \
           'V2lEnV+CJd9+jJlxXmMr5dW14YCqwgbFpO8FNvJxwwM4TPWPo5QalEsRMAcusXpi58/QUEWPL0AK1ThM5oQC' \
           'UyXPoPINkdd922VBw4XgTV9zDGWWFrgjIQs4vwvOg6xr+6gbCTqE+DYhlMGX0CF2OknK5gQ2JrkDh/W6TOEb' \
           'YDeVecKbJtyNXiCfGmW7V93J2hDus1bDfhxWbIZVYDXITA7Lo6E0Ktgg9eB4KWuR44aj7ppBVPazhQH7/M/K' \
           'gWe9X1qAg8XypT6nxIMJH+T94QCsLvj29IYwZxyO9/F8vCbO9tX5/wDGjEZ7vrgFZwAAAABJRU5ErkJggg=='


def get_favicon_16x16_data():
    return 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAABNVBMVEVisTRhsTReqzVbpTVXoDdVnTdSlzhR' \
           'ljgvXkAuXUAtWkErV0EzZj40Zj85bz0lTkMkTUMkT0MmTUIkS0IjTEIhSUMkS0IkTEIkTUIlTUIkTkMlTkMc' \
           'QUQcP0UfQ0QdQ0QfREQgRUMiSUMiSUMjSkInU0EkTEMmUEEiR0IiSEMpVkErWT8kTUElTUIUNkYVNEQVMkcR' \
           'M0QSNUYQMUIMMUkVK0AAJEkAM00AMzMAAAAAAACF6i2E6SyD6CyC5i2B5Sx/4i6A4S593S583S520jB00DBy' \
           'yjFxyTFwyDFvxjJtxTFtxDFswzJrwDJqvzJpvjNouzNoujNnuDNLjTlKijpKiTpEfztDfzxAeT0+dz05bj44' \
           'bT44bj82aj81aD8zZT8bPUUbPkUcP0UcPUUeQ0UfREQgRkRgJREvAAAAO3RSTlP09PX19vX39u7u7/Dq6ufh' \
           '4eDg4+Pf3Nvb2tnY2NvPv7y6rKupqaGZlpSOiYWETDEkHh0fFQwHCgUBAAcHrskAAADYSURBVHjaPc/ZLkNR' \
           'GIbhz26KjVJpqSKGtjHPc9a7W7OEEhtBjDWUO3XghqQSwVrNTp+j///OXhlrLpdJdg9MLblbxqwPd5RLUDpO' \
           'jK66YWMwTqRpaM0OhZbo3dskljea9+HyAevxHtoWVAjhfQtr5w3CSfUE8BrgvEDQpxRc3eyfH5wenlQuIO39' \
           'Sb9x/8uv+bXvmPSjbABPRZznIkGvxkOo7mJtV+FsQsutcFvBuruG9kWZMY+G5pzxlMp/KPKZSUs2cLrzyMWV' \
           'EyP1OGtlNpvs6p+p5/8DzUo5hMDku9EAAAAASUVORK5CYII='
