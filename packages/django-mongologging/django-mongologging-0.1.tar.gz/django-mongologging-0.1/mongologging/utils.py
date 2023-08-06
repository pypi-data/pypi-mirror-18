from __future__ import absolute_import

import inspect
from celery.app.task import Task as celery_task
from django.contrib.auth.base_user import AbstractBaseUser


def make_log_info(initiator_type, initiator_object, stack_depth=4):
    """
    Preparing basic info for logging

    :param initiator_type: type of initiator
    :type initiator_type: str
    :param initiator_object: Initiator object
    :type initiator_object: django.contrib.auth.models.User
          or celery.app.task.Task
    :param stack_depth: Depth of a stack to find caller method. Default to 4
    :type stack_depth: int
    :return: dictionary with basic log info
    :rtype: dict
    """

    initiator_type = initiator_type.lower()

    if initiator_object is None:
        return {}

    if initiator_type == 'user' and isinstance(initiator_object, AbstractBaseUser):
        initiator_id = initiator_object.id
        initiator_name = getattr(initiator_object, 'username', 'unknown')
    elif initiator_type == 'celery' and isinstance(initiator_object, celery_task):
        initiator_id = initiator_object.request.id
        initiator_name = initiator_object.name
    else:
        raise Exception('only initiator_typs `user` and `celery` are allowed now')

    stack = inspect.stack()
    caller = stack[stack_depth][1] + ':' + str(stack[stack_depth][2]) + ':' + stack[stack_depth][3]
    return {
        'initiator_type': initiator_type,
        'initiator_id': initiator_id,
        'initiator_name': initiator_name,
        'caller': caller
    }
