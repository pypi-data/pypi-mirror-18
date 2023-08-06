import json

from django.http import HttpResponse

from .constants import HTTP_STATUS, ERROR_HTTP_STATUSES, SUCCESS_HTTP_STATUSES


class JsonResponse(HttpResponse):

    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. Types not checked

    :param json_util: Json util which is used for dump. Defaults to standard Python json module
    """

    def __init__(self, data, json_util=json, message='', **kwargs):
        # TODO: maybe edit safe param for check allowed data types

        if 'status' not in kwargs:
            kwargs.setdefault('status', HTTP_STATUS.OK)

        kwargs.setdefault('content_type', 'application/json')
        response_data = {
            'status': {
                'code': kwargs['status'],
                'message': message
            },
        }

        if kwargs['status'] in SUCCESS_HTTP_STATUSES.values():
            response_data.update({'data': data})
        elif kwargs['status'] in ERROR_HTTP_STATUSES.values():
            response_data.update({'error': data})
        else:
            raise Exception('this status is not supported by this version of JsonResponse.'
                            'Maybe you need to edit  common.constants file')

        super(JsonResponse, self).__init__(content=json_util.dumps(response_data), **kwargs)
