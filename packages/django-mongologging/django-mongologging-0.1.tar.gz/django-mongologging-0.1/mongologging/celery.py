from __future__ import absolute_import

from .utils import make_log_info
from celery import current_task


class CeleryInitiator(object):
    """
    Always have access to the current celery task
    """
    INITIATOR_TYPE = 'Celery'
    __initiators = {}

    @classmethod
    def get_current_initiator(cls, default=None):
        """
        Retrieve task info
        """
        crt = current_task
        if crt:
            return cls.__initiators.get(crt.request.id, default)

    @classmethod
    def set_current_initiator(cls, task):
        """
        Store task info
        """
        crt = current_task
        if crt:
            cls.__initiators[crt.request.id] = task

    @classmethod
    def del_current_initiator(cls):
        """
        Delete task info
        """
        crt = current_task
        if crt:
            cls.__initiators.pop(crt.request.id, None)

    @classmethod
    def get_info(cls):
        """
        Get initiator info
        """
        return make_log_info(cls.INITIATOR_TYPE, cls.get_current_initiator())
