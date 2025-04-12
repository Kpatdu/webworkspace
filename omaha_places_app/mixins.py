import os
from dotenv import load_dotenv
from urllib.parse import unquote, urlencode

from .models import Restaurant, Place

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

dotenv_path = r'omaha_places_app\cache\googleapi.env'
load_dotenv(dotenv_path=dotenv_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


class RedirectIfNotAuthenticatedMixin(LoginRequiredMixin):
    '''
    Mixin that redirects unauthenticated users to the homepage
    if they attempt to access views requiring login.
    '''

    login_url = '/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            redirect_to = request.get_full_path()

            if not url_has_allowed_host_and_scheme(redirect_to, request.get_host()):
                redirect_to = '/'

            messages.warning(request, 'You must be logged in to access this page.')
            query_string = urlencode({self.redirect_field_name: redirect_to})
            login_redirect_url = f'{self.login_url}?{query_string}'

            return redirect(login_redirect_url)

        return super().dispatch(request, *args, **kwargs)
    

class AllImageAPIKeyMixin:
    '''
    Mixin to get all images with the actual API key.
    '''

    def get_images_with_api_key(self):
        '''
        Function to get all images with the actual API key.
        '''

        restaurant_images = list(Restaurant.objects.exclude(image__isnull=True).exclude(image='N/A').values_list('image', flat=True))
        place_images = list(Place.objects.exclude(image__isnull=True).exclude(image='N/A').values_list('image', flat=True))
        all_images = restaurant_images + place_images

        if GOOGLE_API_KEY:
            all_images_with_api_key = [
                replace_api_key(image, GOOGLE_API_KEY)
                for image in all_images
            ]
        else:
            all_images_with_api_key = all_images
        
        return all_images_with_api_key


class RestaurantImageAPIKeyMixin:
    '''
    Mixin to get all restaurant images with the actual API key.
    '''

    def get_restaurant_images_with_api_key(self):
        '''
        Function to get all restaurant images and categorized restaurant images with the actual API key.
        '''

        restaurant_images = list(Restaurant.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))
        selected_category = self.request.GET.get('category', None)

        if selected_category:
            restaurants = Restaurant.objects.filter(predefined_category=selected_category)
        else:
            restaurants = Restaurant.objects.all()

        if GOOGLE_API_KEY:
            restaurants_with_api_key = [
                replace_api_key(image, GOOGLE_API_KEY)
                for image in restaurant_images
            ]

            for restaurant in restaurants:
                if restaurant.image and restaurant.image != 'N/A':
                    restaurant.image = replace_api_key(str(restaurant.image), GOOGLE_API_KEY)

        else:
            restaurants_with_api_key = restaurant_images

        return restaurants_with_api_key, restaurants
    
    def get_restaurant_images_with_api_key_by_id(self):
        '''
        Function to get all restaurant images with the actual API key by pk id.
        '''

        restaurant = Restaurant.objects.get(id=self.kwargs['pk'])

        if GOOGLE_API_KEY and restaurant.image and str(restaurant.image) != 'N/A':
            restaurant.image = replace_api_key(str(restaurant.image), GOOGLE_API_KEY)

        return restaurant
    

class PlaceImageAPIKeyMixin:
    '''
    Mixin to get all place images with the actual API key.
    '''

    def get_place_images_with_api_key(self):
        '''
        Function to get all place images with the actual API key.
        '''

        place_images = list(Place.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))
        selected_category = self.request.GET.get('category', None)

        if selected_category:
            places = Place.objects.filter(predefined_category=selected_category)
        else:
            places = Place.objects.all()

        if GOOGLE_API_KEY:
            places_with_api_key = [
                replace_api_key(image, GOOGLE_API_KEY)
                for image in place_images
            ]

            for place in places:
                if place.image and place.image != 'N/A':
                    place.image = replace_api_key(str(place.image), GOOGLE_API_KEY)
            
        else:
            places_with_api_key = place_images

        return places_with_api_key, places

    def get_place_images_with_api_key_by_id(self):
        '''
        Function to get all place images with the actual API key by pk id.
        '''

        place = Place.objects.get(id=self.kwargs['pk'])

        if GOOGLE_API_KEY and place.image and str(place.image) != 'N/A':
            place.image = replace_api_key(str(place.image), GOOGLE_API_KEY)

        return place


def replace_api_key(image_url, api_key):
    '''
    Function to replace the placeholder "GOOGLE_API_KEY" with the actual API key.
    Also adjusts the maxwidth parameter to 900.
    '''

    image_url = image_url.replace('GOOGLE_API_KEY', api_key)
    image_url = image_url.replace('maxwidth=400', 'maxwidth=900')
    image_url = unquote(image_url)

    return image_url