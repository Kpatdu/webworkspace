from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import *


class HomeView(TemplateView):
    '''
    Class-based view to render the home page.
    '''

    template_name = 'omaha_places_app/home.html'


class RestaurantsView(ListView):
    '''
    Class-based view to display all restaurants (both manually added and CSV-imported).
    '''

    model = Restaurant
    template_name = 'omaha_places_app/all-restaurants.html'
    context_object_name = 'all_restaurants'


class PlacesView(TemplateView):
    '''
    Class-based view to render the places page.
    '''
    
    template_name = 'omaha_places_app/all-places.html'


class AboutUsView(TemplateView):
    '''
    Class-based view to render the about us page.
    '''
    
    template_name = 'omaha_places_app/about.html'


class ContactUsView(TemplateView):
    '''
    Class-based view to render the contact us page.
    '''
    
    template_name = 'omaha_places_app/contact.html'
