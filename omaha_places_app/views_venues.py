from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView

from .models import Restaurant, Place
from .mixins import RestaurantImageAPIKeyMixin, PlaceImageAPIKeyMixin
from .forms import CommentForm


RESTAURANT_CATEGORY_MAPPING = {
    "restaurant, bar, food, point_of_interest, establishment": "Bar",
    "night_club, bar, restaurant, food, point_of_interest, establishment": "Bar",
    "bar, restaurant, food, point_of_interest, establishment": "Bar",
    "meal_takeaway, bar, restaurant, food, point_of_interest, establishment": "Bar",
    "bakery, bar, store, restaurant, food, point_of_interest, establishment": "Bar",
    "bar, point_of_interest, establishment": "Bar",
    "night_club, bar, point_of_interest, establishment": "Bar",
    "night_club, bar, store, point_of_interest, establishment": "Bar",
    "bowling_alley, bar, point_of_interest, establishment": "Bar",
    "bar, store, restaurant, food, point_of_interest, establishment": "Bar",
    "bar, liquor_store, night_club, point_of_interest, store, establishment": "Bar",
    "bar, restaurant, point_of_interest, food, establishment": "Bar",
    "bar, liquor_store, point_of_interest, store, establishment": "Bar",
    "bar, point_of_interest, store, establishment": "Bar",
    "bar, point_of_interest, food, establishment": "Bar",
    "restaurant, bar, point_of_interest, food, establishment": "Bar",
    "bar, liquor_store, restaurant, point_of_interest, food, store, establishment": "Bar",
    "cafe, bakery, bar, store, food, night_club, point_of_interest, establishment": "Bar",
    
    "restaurant, food, point_of_interest, establishment": "Restaurant",
    "meal_takeaway, restaurant, food, point_of_interest, establishment": "Restaurant",
    "meal_delivery, meal_takeaway, restaurant, food, point_of_interest, establishment": "Restaurant",
    "meal_takeaway, meal_delivery, restaurant, food, point_of_interest, establishment": "Restaurant",
    "store, restaurant, food, point_of_interest, establishment": "Restaurant",
    "restaurant, cafe, food, point_of_interest, establishment": "Restaurant",
    "restaurant, bakery, cafe, store, food, point_of_interest, establishment": "Restaurant",

    "cafe, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, store, food, point_of_interest, establishment": "Cafe",
    "book_store, cafe, store, food, point_of_interest, establishment": "Cafe",
    "bakery, cafe, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, meal_takeaway, bakery, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, bakery, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "book_store, cafe, church, place_of_worship, store, food, point_of_interest, establishment": "Cafe",
    "gas_station, bakery, cafe, liquor_store, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "meal_takeaway, bakery, cafe, store, restaurant, food, point_of_interest, establishment": "Cafe",
    "cafe, food, point_of_interest, establishment": "Cafe",

    "meal_takeaway, bakery, grocery_or_supermarket, store, restaurant, food, point_of_interest, establishment": "Grocery-Bakery",
    "department_store, hardware_store, bakery, grocery_or_supermarket, furniture_store, home_goods_store, clothing_store, electronics_store, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, florist, bakery, liquor_store, health, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, bakery, supermarket, health, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, electronics_store, liquor_store, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, supermarket, grocery_or_supermarket, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, department_store, bakery, supermarket, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "bakery, store, restaurant, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, supermarket, bakery, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, bakery, store, food, point_of_interest, establishment": "Grocery-Bakery",
    "grocery_or_supermarket, supermarket, bakery, pharmacy, liquor_store, florist, health, store, food, point_of_interest, establishment": "Grocery-Bakery",

    "gas_station, cafe, moving_company, car_repair, store, restaurant, food, point_of_interest, establishment": "Gas-Station",

     "movie_theater, meal_takeaway, restaurant, food, point_of_interest, establishment": "Others",
}

PLACE_CATEGORY_MAPPING = {
    "amusement_park, point_of_interest, clothing_store, store, establishment": "Park",
    "amusement_park, point_of_interest, establishment": "Park",
    "park, point_of_interest, establishment": "Park",
    "park, tourist_attraction, point_of_interest, establishment": "Park",
    "funeral_home, cemetery, park, point_of_interest, establishment": "Park",
    "museum, tourist_attraction, park, point_of_interest, establishment": "Park",
    "store, park, point_of_interest, establishment": "Park",
    "tourist_attraction, amusement_park, point_of_interest, establishment": "Park",
    
    "art_gallery, furniture_store, home_goods_store, point_of_interest, store, establishment": "Store",
    "art_gallery, furniture_store, home_goods_store, store, point_of_interest, establishment": "Store",
    "art_gallery, point_of_interest, store, establishment": "Store",
    "art_gallery, store, point_of_interest, establishment": "Store",
    "book_store, library, point_of_interest, store, establishment": "Store",
    "clothing_store, store, point_of_interest, establishment": "Store",
    "department_store, hardware_store, electronics_store, bakery, furniture_store, home_goods_store, grocery_or_supermarket, clothing_store, store, food, point_of_interest, establishment": "Store",
    "department_store, shoe_store, electronics_store, furniture_store, home_goods_store, clothing_store, store, point_of_interest, establishment": "Store",
    "electronics_store, museum, point_of_interest, store, establishment": "Store",
    "furniture_store, art_gallery, home_goods_store, point_of_interest, store, establishment": "Store",
    "furniture_store, electronics_store, home_goods_store, store, point_of_interest, establishment": "Store",
    "store, point_of_interest, establishment": "Store",
    
    "art_gallery, bar, cafe, restaurant, point_of_interest, food, store, establishment": "Bar",
    "art_gallery, bar, point_of_interest, establishment": "Bar",
    "restaurant, bar, food, point_of_interest, establishment": "Bar",
    
    "art_gallery, museum, point_of_interest, establishment": "Museum-Theater",
    "art_gallery, tourist_attraction, point_of_interest, establishment": "Museum-Theater",
    "movie_theater, meal_takeaway, restaurant, food, point_of_interest, establishment": "Museum-Theater",
    "movie_theater, point_of_interest, establishment": "Museum-Theater",
    "museum, point_of_interest, establishment": "Museum-Theater",
    "museum, tourist_attraction, point_of_interest, establishment": "Museum-Theater",
    "tourist_attraction, art_gallery, point_of_interest, establishment": "Museum-Theater",
    "tourist_attraction, museum, point_of_interest, establishment": "Museum-Theater",
    "art_gallery, restaurant, point_of_interest, food, establishment": "Museum-Theater",
    
    "art_gallery, school, point_of_interest, establishment": "School",
    "school, point_of_interest, establishment": "School",
    "secondary_school, school, point_of_interest, establishment": "School",
    "university, health, point_of_interest, establishment": "School",
    "university, point_of_interest, establishment": "School",
    
    "art_gallery, health, point_of_interest, establishment": "TravelAgent-Health",
    "beauty_salon, art_gallery, gym, health, point_of_interest, establishment": "TravelAgent-Health",
    "hospital, health, point_of_interest, establishment": "TravelAgent-Health",
    "tourist_attraction, travel_agency, point_of_interest, establishment": "TravelAgent-Health",
    
    "casino, lodging, point_of_interest, establishment": "Lodging",
    "lodging, point_of_interest, establishment": "Lodging",
    
    "zoo, point_of_interest, establishment": "Zoo",
    "zoo, tourist_attraction, point_of_interest, establishment": "Zoo",
    "zoo, park, point_of_interest, establishment": "Zoo",
    "zoo, tourist_attraction, park, point_of_interest, establishment": "Zoo",
    
    "mosque, tourist_attraction, place_of_worship, point_of_interest, establishment": "Mosque",
    
    "art_gallery, local_government_office, point_of_interest, establishment": "Others",
    "art_gallery, point_of_interest, establishment": "Others",
    "library, point_of_interest, establishment": "Others",
    "local_government_office, point_of_interest, establishment": "Others",
    "point_of_interest, establishment": "Others",
    "tourist_attraction, point_of_interest, establishment": "Others"
}


class RestaurantsView(RestaurantImageAPIKeyMixin, ListView):
    '''
    Class-based view to display the restaurant home page.
    '''

    model = Restaurant
    template_name = 'omaha_places_app/home-restaurants.html'
    context_object_name = 'home_restaurants'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predefined_category = sorted(
            set(Restaurant.objects.values_list('predefined_category', flat=True).distinct()),
            key=lambda x: (x is None, str(x).lower())
        )

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
        predefined_category = sorted(
            set(Restaurant.objects.values_list('predefined_category', flat=True).distinct()),
            key=lambda x: (x is None, str(x).lower())
        )
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
        predefined_category = sorted(
            set(Place.objects.values_list('predefined_category', flat=True).distinct()),
            key=lambda x: (x is None, str(x).lower())
        )


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
        predefined_category = sorted(
            set(Place.objects.values_list('predefined_category', flat=True).distinct()),
            key=lambda x: (x is None, str(x).lower())
        )
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
