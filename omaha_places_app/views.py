from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login

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


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "omaha_places_app/register.html", {
        "form" : form
    })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "omaha_places_app/login.html", {
        "form" : form
    })

def logout_view(request):
    logout(request)
    return redirect("login")