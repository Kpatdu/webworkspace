from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'), # Home
    path('about/', views.AboutUsView.as_view(), name = 'about'), # About Us

    path('restaurants/home/', views.RestaurantsView.as_view(), name = 'home_restaurants'), # List Restaurants
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name = 'restaurant_detail'), # Individual Restaurant
    path('places/home/', views.PlacesView.as_view(), name = 'home_places'), # List Places
    path('places/<int:pk>/', views.PlaceDetailView.as_view(), name = 'place_detail'), # IndividualPlace

    path('locations/', views.LocationsView.as_view(), name = 'locations') # Locations
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)