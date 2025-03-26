from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *

import random


class HomeView(TemplateView):
    template_name = 'omaha_places_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all restaurant and place images
        restaurant_images = list(Restaurant.objects.exclude(image__isnull = True).exclude(image = '').values_list('image', flat = True))
        place_images = list(Place.objects.exclude(image__isnull = True).exclude(image = '').values_list('image', flat = True))

        all_images = restaurant_images + place_images

        # Select a random image if available
        context['random_image'] = random.choice(all_images) if all_images else None

        return context


class RestaurantsView(ListView):
    '''
    Class-based view to display all restaurants (both manually added and CSV-imported).
    '''

    model = Restaurant
    template_name = 'omaha_places_app/all-restaurants.html'
    context_object_name = 'all_restaurants'


class RestaurantDetailView(TemplateView):
    '''
    Class-based view to display the details of a single restaurant.
    '''

    template_name = 'omaha_places_app/restaurant.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(id=self.kwargs['pk'])

        return context


class PlacesView(ListView):
    '''
    Class-based view to render the places page.
    '''
    
    model = Place
    template_name = 'omaha_places_app/all-places.html'
    context_object_name = 'all_places'


class PlaceDetailView(TemplateView):
    '''
    Class-based view to display the details of a single place.
    '''

    template_name = 'omaha_places_app/place.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['place'] = Place.objects.get(id=self.kwargs['pk'])

        return context


class AboutUsView(TemplateView):
    '''
    Class-based view to render the about us page.
    '''
    
    template_name = 'omaha_places_app/about.html'

