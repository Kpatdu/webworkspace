from .mixins import RestaurantImageAPIKeyMixin, PlaceImageAPIKeyMixin

from django.shortcuts import render
from django.views.generic import TemplateView


class LocationsView(TemplateView, RestaurantImageAPIKeyMixin, PlaceImageAPIKeyMixin):
    '''
    Class-based view for displaying all locations (restaurants and places).
    '''

    template_name = 'omaha_places_app/all-locations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the restaurant and place images with the API key
        restaurants = self.get_restaurant_images_with_api_key()[1]
        places = self.get_place_images_with_api_key()[1]

        context['all_restaurants'] = restaurants
        context['all_places'] = places

        # Parse all unique categories from restaurant and place objects
        category_set = set()
        for r in restaurants:
            if r.category:
                category_set.update([cat.strip() for cat in r.category.split(',')])
        for p in places:
            if p.category:
                category_set.update([cat.strip() for cat in p.category.split(',')])
        context['all_categories'] = sorted(list(category_set))

        # Get filters from request and pass them to the context
        context['selected_categories'] = self.request.GET.getlist('cat_contains')

        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        # Get filters from request
        name_contains = request.GET.get('name_contains')
        cat_contains_list = request.GET.getlist('cat_contains')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        rating_min = request.GET.get('rating_min')
        rating_max = request.GET.get('rating_max')
        description_contains = request.GET.get('description_contains')

        # Get the restaurant and place images with the API key
        restaurants = self.get_restaurant_images_with_api_key()[1]
        places = self.get_place_images_with_api_key()[1]

        # Start with all items
        restaurants = context['all_restaurants']
        places = context['all_places']

        # Apply filters
        if name_contains:
            restaurants = restaurants.filter(name__icontains=name_contains)
            places = places.filter(name__icontains=name_contains)

        if cat_contains_list:
            for cat in cat_contains_list:
                restaurants = restaurants.filter(category__icontains=cat)
                places = places.filter(category__icontains=cat)

        if price_min or price_max:
            def price_valid(obj):
                try:
                    price_str = obj.price_level
                    price = float(price_str) if price_str not in [None, '', 'N/A'] else 0
                    if price_min and price < float(price_min):
                        return False
                    if price_max and price > float(price_max):
                        return False
                    return True
                except (ValueError, TypeError):
                    return False
            
            restaurants = list(filter(price_valid, restaurants))
            places = list(filter(price_valid, places))

        if rating_min:
            restaurants = restaurants.filter(rating__gte=rating_min)
            places = places.filter(rating__gte=rating_min)
        if rating_max:
            restaurants = restaurants.filter(rating__lte=rating_max)
            places = places.filter(rating__lte=rating_max)

        if description_contains:
            restaurants = restaurants.filter(description__icontains=description_contains)
            places = places.filter(description__icontains=description_contains)

        # Pass filtered results
        context['all_restaurants'] = restaurants
        context['all_places'] = places

        return render(request, self.template_name, context)