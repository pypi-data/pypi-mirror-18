import importlib
import logging
import math

import pymongo
from bson import json_util
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from .http.constants import HTTP_STATUS
from http.decorators import ajax_view
from http.utils import JsonResponse
from .connection import logs, LOGS_PAGE_SIZE
from .forms import LogFilterForm

logger = logging.getLogger(__name__)


if hasattr(settings, 'MONGO_LOGGING_VIEW_ACCESS_DECORATOR'):
    try:
        user_access = importlib.import_module(settings.MONGO_LOGGING_VIEW_ACCESS_DECORATOR)
    except ImportError as err:
        raise ImportError('Cannot find this decorator: {0}'.format(err))
else:
    access = getattr(settings, 'MONGO_LOGGING_ACCESS', '')
    user_access = lambda user: getattr(user, access, True)


@login_required
@user_passes_test(user_access)
def logs_page(request):
    """
    Rendering main page with logging form

    :param request: Django HTTPRequest
    :return: rendered logging page with form
    """
    form = LogFilterForm()
    return render(request, 'filter.html', {'form': form})


@login_required
@user_passes_test(user_access)
@ajax_view(methods=['GET', 'POST'])
def logs_filter(request):
    """
    View for ajax POST request for filtering logs from MongoDB.

    :param request: Django HttpRequest
    :return: response in json format witl logs and additional keys for simple paging
    :rtype: Django HttpResponse
    """
    form = LogFilterForm(request.json)
    if form.is_valid():
        page = request.json.get('page', 1)
        if not isinstance(page, int) or page < 1:
            return JsonResponse('page should be a positive number', status=HTTP_STATUS.BadRequest)

        try:
            queryset = logs.find(form.cleaned_data)
            total = queryset.count()
        except pymongo.errors.PyMongoError as err:
            logger.error('MongoDB error', extra={'error': err})
            return JsonResponse('MongoDB error', status=HTTP_STATUS.ServerError)

        total_pages = int(math.ceil(float(total) / LOGS_PAGE_SIZE))
        if 1 < page > total_pages:
            page = total_pages

        try:
            filtered_logs = queryset.skip(LOGS_PAGE_SIZE * (page - 1)).limit(LOGS_PAGE_SIZE)
        except pymongo.errors.PyMongoError as err:
            logger.error('MongoDB error', extra={'error': err})
            return JsonResponse('MongoDB error', status=HTTP_STATUS.BadRequest)

        return JsonResponse(
            data={
                'logs': filtered_logs, 'page': page, 'page_size': LOGS_PAGE_SIZE,
                'total': total, 'total_pages': total_pages,
                'has_prev_page': page > 1,
                'has_next_page': page < total_pages
            },
            json_util=json_util,
        )
    return JsonResponse(form.errors.as_json(), status=HTTP_STATUS.BadRequest)
