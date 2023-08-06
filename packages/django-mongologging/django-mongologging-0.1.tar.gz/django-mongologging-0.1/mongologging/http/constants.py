SUCCESS_HTTP_STATUSES = {
    u'OK': 200,
    u'Created': 201,
}

ERROR_HTTP_STATUSES = {
    u'BadRequest': 400,
    u'Unauthorized': 401,
    u'Forbidden': 403,
    u'NotFound': 404,
    u'MethodNotAllowed': 405,
    u'ServerError': 500,
}

SAFE_HTTP_METHODS = ('GET', 'HEAD')
UNSAFE_HTTP_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

HTTP_STATUS = SUCCESS_HTTP_STATUSES.copy()
HTTP_STATUS.update(ERROR_HTTP_STATUSES)
