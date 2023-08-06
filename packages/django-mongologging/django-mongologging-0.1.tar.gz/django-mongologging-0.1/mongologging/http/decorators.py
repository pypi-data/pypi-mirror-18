import functools
import json
from .constants import HTTP_STATUS

from django.http import HttpResponse


def ajax_view(methods):
    """
    Decorator for ajax views

    :param methods: method names ('GET', 'POST', ...)
    :type methods: list of str
    :return: view_func with request.body changed from json to dict or 400: BadRequest or 405: Method not allowed errors
    :rtype: function which returns HttpRequest or HttpRequest with status=400 or status=405
    """
    def _ajax_method(view_func):
        @functools.wraps(view_func)
        def _wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponse(status=HTTP_STATUS.BadRequest)
            if request.method not in methods:
                return HttpResponse(status=HTTP_STATUS.MethodNotAllowed)
            setattr(request, 'json', json.loads(request.body))
            return view_func(request, *args, **kwargs)

        return _wrap
    return _ajax_method