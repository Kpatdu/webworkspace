from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    '''
    Class-based view to render the home page.
    '''

    template_name = 'omaha_places_app/home.html'


class RestaurantsView(TemplateView):
    '''
    Class-based view to render the restaurants page.
    '''
    
    template_name = 'omaha_places_app/restaurants.html'


class PlacesView(TemplateView):
    '''
    Class-based view to render the places page.
    '''
    
    template_name = 'omaha_places_app/places.html'


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
