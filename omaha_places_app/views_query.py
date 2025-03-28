from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *

import os
from dotenv import load_dotenv
from urllib.parse import unquote


class LocationsView(TemplateView):
    '''
    Class-based view to display all restaurants and places together.
    '''
    
    template_name = 'omaha_places_app/all-locations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_restaurants'] = Restaurant.objects.all()
        context['all_places'] = Place.objects.all()

        return context
