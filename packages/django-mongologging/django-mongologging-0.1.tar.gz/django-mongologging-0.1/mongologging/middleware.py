import threading
from .utils import make_log_info

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class UserInitiatorMiddleware(MiddlewareMixin):
    """
    Always have access to the current user
    """
    INITIATOR_TYPE = 'User'
    __initiators = {}

    def process_request(self, request):
        """
        Store user info
        """
        self.__class__.set_current_initiator(request.user)

    def process_response(self, request, response):
        """
        Delete user info
        """
        self.__class__.del_current_initiator()
        return response

    def process_exception(self, request, exception):
        """
        Delete user info
        """
        self.__class__.del_current_initiator()

    @classmethod
    def get_current_initiator(cls, default=None):
        """
        Retrieve user info
        """
        return cls.__initiators.get(threading.current_thread(), default)

    @classmethod
    def set_current_initiator(cls, user):
        """
        Store user info
        """
        cls.__initiators[threading.current_thread()] = user

    @classmethod
    def del_current_initiator(cls):
        """
        Delete user info
        """
        cls.__initiators.pop(threading.current_thread(), None)

    @classmethod
    def get_info(cls):
        """
        Delete initiator info
        """
        return make_log_info(cls.INITIATOR_TYPE, cls.get_current_initiator())
