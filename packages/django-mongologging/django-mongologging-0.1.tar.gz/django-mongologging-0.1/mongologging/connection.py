import logging

from django.conf import settings
from pymongo import MongoClient

logger = logging.getLogger(__name__)


# TODO: Specifying fields not actually implemented yet

DEFAULT_LOG_FIELDS = {
    u'caller', u'initiator_type', u'name',
    u'changes', u'object_type', u'BasicUser',
    u'object_id', u'datetime', u'id'
}

LOG_FIELDS = set(getattr(settings, 'MONGO_LOGGING_FIELDS', DEFAULT_LOG_FIELDS))

if not LOG_FIELDS.issubset(DEFAULT_LOG_FIELDS):
    raise ValueError('Only log {0} fields are allowed'.format(','.join(DEFAULT_LOG_FIELDS)))


CONNECTION_SETTINGS = {
    'host': getattr(settings, 'MONGO_DATABASE_HOST', 'localhost'),
    'port': getattr(settings, 'MONGO_DATABASE_PORT', 27017),
    'connect': False
}

LOGS_PAGE_SIZE = getattr(settings, 'LOGS_PAGE_SIZE', 100)

connection = MongoClient(**CONNECTION_SETTINGS)
db = connection[getattr(settings, 'MONGO_DATABASE_NAME', 'logs_db')]
logs = db[getattr(settings, 'MONGO_LOGGING_COLLECTION', 'django_logs')]
