from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'), # Home
    path('restaurants/all/', views.RestaurantsView.as_view(), name = 'all_restaurants'), # List Restaurants
    path('places/all/', views.PlacesView.as_view(), name = 'all_places'), # List Places
    path('about/', views.AboutUsView.as_view(), name = 'about'), # About Us
    path('contact/', views.ContactUsView.as_view(), name = 'contact'), # Contact Us
]
