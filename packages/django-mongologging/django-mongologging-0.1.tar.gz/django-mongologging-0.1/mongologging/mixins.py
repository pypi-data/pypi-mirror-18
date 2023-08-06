import logging
import datetime
from socket import error as socket_error

from django.db.models.fields.related import ManyToManyField
from django.conf import settings
from .tasks import logging_to_mongo
from .middleware import UserInitiatorMiddleware
from .celery import CeleryInitiator

logger = logging.getLogger(__name__)


class LoggingMixin(object):
    """
    A model mixin to find fields that have been changed
    """

    EXCEPT_FIELDS = ['password', 'last_login']

    def __init__(self, *args, **kwargs):
        """
        Init method. Setting first copy and except fields (default: password)

        :param args:
        :param kwargs:
        """
        super(LoggingMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        """
        Property to find difference in model fields

        :return: dictionary {field: (was, now)}
        :rtype: dict
        """
        initial = self.__initial
        current = self._dict
        diffs = {field: (was, current[field]) for field, was in initial.items()
                 if field not in self.EXCEPT_FIELDS and was != current[field]}
        return diffs

    @property
    def has_changed(self):
        """
        Property to find out if there were any changes in a model

        :return: True if there are some changes, False - otherwise
        :rtype: bool
        """
        return bool(self.diff)

    @property
    def changed_fields(self):
        """
        Property to find out changed fields in a model

        :return: list of changed field
        :rtype: list
        """
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.

        :return: tuple(was, now)
        :rtype: tuple
        """
        return self.diff.get(field_name, None)

    def log_data(self, data):
        """
        Logging data to MongoDB via celery

        :param data: dictionary containing logging info to add to MongoDB
        :type data: dict
        :return:
        """
        if not isinstance(data, dict):
            raise Exception('Only argument of type `dict` is supported')

        if self.has_changed:
            data.update(
                {
                    'changes': self.diff,
                    'object_type': self.__class__.__name__,
                    'object_id': self.id,
                }
            )

            if getattr(settings, 'AUTO_FIND_INITIATOR', True):

                data.update(CeleryInitiator.get_info())

                data.update(UserInitiatorMiddleware.get_info())

            if hasattr(settings, 'BROKER_URL'):
                try:
                    logging_to_mongo.apply_async(args=(data,))

                except socket_error as serr:
                    logger.error('RabbitMQ connection error', extra={'error': serr})
                    logger.error('Trying to write log in a sync way', extra={'error': serr})
                    logging_to_mongo(data)
            else:
                logging_to_mongo(data)

            self.__initial = self._dict

        else:
            logger.info('No changes found, nothing to log')

    def to_dict(self):
        """
        Convert model to dict extending django.forms.models.model_to_dict
        for not editable datetime field
        :return:
        """
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
            if isinstance(data[f.name], datetime.datetime):
                data[f.name] = data[f.name].strftime('%Y-%m-%d %H:%M:%S.%f')
        return data

    @property
    def _dict(self):
        """
        Property to convert model to dict

        :return: dictionary {field: value}
        :rtype: dict
        """
        return self.to_dict()
