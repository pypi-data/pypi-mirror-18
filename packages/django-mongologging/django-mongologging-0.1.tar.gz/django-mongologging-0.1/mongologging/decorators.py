import functools
from .celery import CeleryInitiator


def log_this_task(task_fun):
    """
    Decorator to log events inside celery tasks
    :param task_fun: func
    :return: celery task function
    """
    @functools.wraps(task_fun)
    def outer(self, *args, **kwargs):
        CeleryInitiator.set_current_initiator(self)
        celery_task = task_fun(self)
        CeleryInitiator.del_current_initiator()
        return celery_task

    return outer
