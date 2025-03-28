from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *

import os
from dotenv import load_dotenv
from urllib.parse import unquote


class RestaurantsView(ListView):
    '''
    Class-based view to display restaurants.
    '''

    model = Restaurant
    template_name = 'omaha_places_app/home-restaurants.html'
    context_object_name = 'home_restaurants'


class RestaurantDetailView(TemplateView):
    '''
    Class-based view to display the details of a single restaurant.
    '''

    template_name = 'omaha_places_app/restaurant.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(id = self.kwargs['pk'])

        return context


class PlacesView(ListView):
    '''
    Class-based view to display places.
    '''
    
    model = Place
    template_name = 'omaha_places_app/home-places.html'
    context_object_name = 'home_places'


class PlaceDetailView(TemplateView):
    '''
    Class-based view to display the details of a single place.
    '''

    template_name = 'omaha_places_app/place.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place'] = Place.objects.get(id = self.kwargs['pk'])

        return context
