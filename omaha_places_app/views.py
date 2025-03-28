from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *

import os
from dotenv import load_dotenv
from urllib.parse import unquote


class HomeView(TemplateView):
    '''
    Class-based view to render the home page.
    '''

    template_name = 'omaha_places_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all restaurant and place images
        restaurant_images = list(Restaurant.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))
        place_images = list(Place.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))

        all_images = restaurant_images + place_images

        dotenv_path = r'omaha_places_app\cache\googleapi.env'
        load_dotenv(dotenv_path=dotenv_path)
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

        # Ensure the API key is correctly replaced
        if GOOGLE_API_KEY:
            all_images_with_api_key = [
                self.replace_api_key(image, GOOGLE_API_KEY)
                for image in all_images
            ]
        else:
            all_images_with_api_key = all_images  # If no API key, use the image URLs as is

        context['all_images'] = all_images_with_api_key

        return context

    def replace_api_key(self, image_url, api_key):
        '''
        Replace the placeholder GOOGLE_API_KEY in the image URL with the actual API key.
        '''

        image_url = image_url.replace('GOOGLE_API_KEY', api_key)
        image_url = unquote(image_url)

        return image_url



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
