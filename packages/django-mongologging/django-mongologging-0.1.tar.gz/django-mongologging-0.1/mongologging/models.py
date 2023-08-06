from django.db import models
from .mixins import LoggingMixin


class LoggingModel(models.Model, LoggingMixin):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Saves model, sets initial state and logging to mongo

        """

        log_data = kwargs.pop('log_data', {})

        super(LoggingModel, self).save(*args, **kwargs)

        self.log_data(log_data)
