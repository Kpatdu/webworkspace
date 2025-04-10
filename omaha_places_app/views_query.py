from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


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
    
    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            q = request.POST['q']
            context['all_restaurants'] = Restaurant.objects.filter(name__contains=q) | Restaurant.objects.filter(category__contains=q)
            context['all_places'] = Place.objects.filter(name__contains=q) | Place.objects.filter(category__contains=q)
            return render(request, self.template_name, context)
        
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'GET':
            name_contains_query = request.GET.get('name_contains')
            cat_contains_query = request.GET.get('cat_contains')
            price_min = request.GET.get('price_min')
            price_max = request.GET.get('price_max')
            rating_min = request.GET.get('rating_min')
            rating_max = request.GET.get('rating_max')

            context['all_restaurants'] = Restaurant.objects.all()
            context['all_places'] = Place.objects.all()


            if name_contains_query != '' and name_contains_query is not None:
                context['all_restaurants'] = context['all_restaurants'].filter(name__contains=name_contains_query)
                context['all_places'] = context['all_places'].filter(name__contains=name_contains_query)
            if cat_contains_query != '' and cat_contains_query is not None:
                print('hi')
                context['all_restaurants'] = context['all_restaurants'].filter(category__contains=cat_contains_query)
                context['all_places'] = context['all_places'].filter(category__contains=cat_contains_query)
            if price_min != '' and price_min is not None:
                context['all_restaurants'] = context['all_restaurants'].filter(price__gte=price_min)
                context['all_places'] = context['all_places'].filter(price__gte=price_min)
            if price_max != '' and price_max is not None:
                context['all_restaurants'] = context['all_restaurants'].filter(price__lte=price_max)
                context['all_places'] = context['all_places'].filter(price__lte=price_max)
            if rating_min != '' and rating_min is not None:
                context['all_restaurants'] = context['all_restaurants'].filter(rating__gte=rating_min)
                context['all_places'] = context['all_places'].filter(rating__gte=rating_min)
            if rating_max != '' and rating_max is not None:
                context['all_restaurants'] = context['all_restaurants'].filter(rating__lte=rating_max)
                context['all_places'] = context['all_places'].filter(rating__lte=rating_max)
            

            return render(request, self.template_name, context)
