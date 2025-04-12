from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Restaurant, Place


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