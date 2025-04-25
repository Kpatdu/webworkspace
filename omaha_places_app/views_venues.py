from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from .models import Restaurant, Place
from .mixins import RestaurantImageAPIKeyMixin, PlaceImageAPIKeyMixin
from .forms import CommentForm


class RestaurantsView(RestaurantImageAPIKeyMixin, ListView):
    '''
    Class-based view to display the restaurant home page.
    '''

    model = Restaurant
    template_name = 'omaha_places_app/home-restaurants.html'
    context_object_name = 'home_restaurants'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predefined_category = Restaurant.objects.values_list('predefined_category', flat = True).distinct()

        context['predefined_category'] = predefined_category
        context['restaurant_images'] = self.get_restaurant_images_with_api_key()[0]

        return context


class RestaurantsViewAll(RestaurantImageAPIKeyMixin, TemplateView):
    '''
    Class-based view to display all restaurants.
    '''

    model = Restaurant
    template_name = 'omaha_places_app/all-restaurants.html'
    context_object_name = 'all_restaurants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predefined_category = Restaurant.objects.values_list('predefined_category', flat = True).distinct()
        selected_category = self.request.GET.get('category', None)

        restaurants_with_api_key, restaurants = self.get_restaurant_images_with_api_key()
        
        context['restaurant_images'] = restaurants_with_api_key
        context['selected_category'] = selected_category
        context['predefined_category'] = predefined_category
        context['all_restaurants'] = restaurants

        return context
    

class RestaurantDetailView(RestaurantImageAPIKeyMixin, TemplateView):
    '''
    Class-based view to display the details of a single restaurant.
    '''

    template_name = 'omaha_places_app/restaurant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_restaurant_images_with_api_key_by_id()

        context['restaurant'] = restaurant
        context['comments'] = restaurant.comments.all().order_by('-created_at')
        
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        else:
            context['comment_form'] = None

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.user = request.user
            comment.restaurant = restaurant
            comment.save()

        return redirect(request.path)


class PlacesView(PlaceImageAPIKeyMixin, ListView):
    '''
    Class-based view to display the places homepage.
    '''
    
    model = Place
    template_name = 'omaha_places_app/home-places.html'
    context_object_name = 'home_places'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predefined_category = Place.objects.values_list('predefined_category', flat = True).distinct()

        context['place_images'] = self.get_place_images_with_api_key()[0]
        context['predefined_category'] = predefined_category

        return context
    

class PlacesViewAll(PlaceImageAPIKeyMixin, ListView):
    '''
    Class-based view to display all places in details.
    '''

    model = Place
    template_name = 'omaha_places_app/all-places.html'
    context_object_name = 'all_places'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predefined_category = Place.objects.values_list('predefined_category', flat = True).distinct()
        selected_category = self.request.GET.get('category', None)
        
        places_with_api_key, places = self.get_place_images_with_api_key()

        context['predefined_category'] = predefined_category
        context['selected_category'] = selected_category
        context['all_places'] = places
        context['place_images'] = places_with_api_key

        return context


class PlaceDetailView(PlaceImageAPIKeyMixin, TemplateView):
    '''
    Class-based view to display the details of a single place.
    '''

    template_name = 'omaha_places_app/place.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place = self.get_place_images_with_api_key_by_id()

        context['place'] = place

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        place = Place.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.user = request.user
            comment.place = place
            comment.save()

        return redirect(request.path)
