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
        restaurant_images = list(Restaurant.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))
        place_images = list(Place.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))

        all_images = restaurant_images + place_images
        

        # Select a random image; Header
        context['random_image_1'] = random.choice(all_images) if all_images else None
        context['random_image_2'] = random.choice(all_images) if all_images else None
        context['random_image_3'] = random.choice(all_images) if all_images else None

        # Select a random image
        context['random_image_4'] = random.choice(all_images) if all_images else None
        context['random_image_5'] = random.choice(all_images) if all_images else None
        context['random_image_6'] = random.choice(all_images) if all_images else None
        context['random_image_7'] = random.choice(all_images) if all_images else None

        return context


class AboutUsView(TemplateView):
    '''
    Class-based view to render the about us page.
    '''
    
    template_name = 'omaha_places_app/about.html'





#########################################################################################





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
        context['restaurant'] = Restaurant.objects.get(id=self.kwargs['pk'])

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
        context['place'] = Place.objects.get(id=self.kwargs['pk'])

        return context





#########################################################################################





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
