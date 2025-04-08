from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
from .models import *

import os
from dotenv import load_dotenv
from omaha_places_app.api_key import replace_api_key


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
                replace_api_key(image, GOOGLE_API_KEY)
                for image in all_images
            ]
        else:
            all_images_with_api_key = all_images

        context['all_images'] = all_images_with_api_key

        return context


class AboutUsView(TemplateView):
    '''
    Class-based view to render the about us page.
    '''
    
    template_name = 'omaha_places_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all restaurant and place images
        restaurant_images = list(Restaurant.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))
        place_images = list(Place.objects.exclude(image__isnull = True).exclude(image = 'N/A').values_list('image', flat = True))
        all_images = restaurant_images + place_images

        dotenv_path = r'omaha_places_app\cache\googleapi.env'
        load_dotenv(dotenv_path=dotenv_path)
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

        if GOOGLE_API_KEY:
            all_images_with_api_key = [
                replace_api_key(image, GOOGLE_API_KEY)
                for image in all_images
            ]
        else:
            all_images_with_api_key = all_images

        context['all_images'] = all_images_with_api_key

        return context


def register_view(request):
    '''
    View to handle user registration.
    '''

    if request.user.is_authenticated:
        return redirect("home")  # Redirect if already logged in
    
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
    '''
    View to handle user login.
    '''

    if request.user.is_authenticated:
        return redirect("home")

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
    '''
    View to handle user logout.
    '''
    
    logout(request)
    return redirect("login")


