from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse


class Restaurant(models.Model):
    '''
    Model for manually adding a restaurant page.
    '''

    name = models.CharField('Restaurant Name', help_text = 'Name of the restaurant', max_length = 100)
    location = models.CharField('Location', help_text = 'Restaurant location.', max_length = 100)
    description = models.TextField('Description', help_text = 'Restaurant description')

    class Meta():
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name