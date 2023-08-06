from __future__ import absolute_import

import datetime
import logging

import pymongo
from celery.decorators import task

from .connection import logs

logger = logging.getLogger(__name__)


@task
def logging_to_mongo(log_data):
    """
    Celery task to logging to MongoDB

    :param self: celery task
    :type self: celery.app.task
    :param log_data: dictinary to with basic logging data to write to MongoDB
    :return:
    """

    log_data.update({'datetime': datetime.datetime.utcnow()})

    try:
        logs.insert(log_data)
        logger.info('Logs inserted into DB')
    except pymongo.errors.PyMongoError as err:
        logger.error("MongoDB error", extra={'error': err})
