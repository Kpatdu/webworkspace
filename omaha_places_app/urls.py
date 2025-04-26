from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, views_query, views_venues, views_event, views_account

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'), # Home
    path('about/', views.AboutUsView.as_view(), name = 'about'), # About Us

    path('restaurants/home/', views_venues.RestaurantsView.as_view(), name = 'home_restaurants'), # List Restaurants
    path('restaurants/all/', views_venues.RestaurantsViewAll.as_view(), name='all_restaurants'),  # List all of Restaurants in categories
    path('restaurants/<int:pk>/', views_venues.RestaurantDetailView.as_view(), name = 'restaurant_detail'), # Individual Restaurant

    path('places/home/', views_venues.PlacesView.as_view(), name = 'home_places'), # List Places
    path('places/all/', views_venues.PlacesViewAll.as_view(), name = 'all_places'), # List all of places in categories
    path('places/<int:pk>/', views_venues.PlaceDetailView.as_view(), name = 'place_detail'), # Individual Places

    path('locations/', views_query.LocationsView.as_view(), name = 'locations'), # Locations

    
    path('register/', views_account.register_view, name = 'register'), # Register
    path('login/', views_account.login_view, name = 'login'), # Login
    path('logout/', views_account.logout_view, name = 'logout'), # Logout

    path('account/', views_account.AccountView.as_view(), name = 'account'), # Account
    path('account/password_reset/', views_account.ResetPasswordView.as_view(), name = 'change_password'), # Password Reset
    path('account/saving_location/', views_account.SaveLocationView.as_view(), name = 'save_location'), # Saved Locations
    path('account/saved_locations/', views_account.SavedLocationListView.as_view(), name = 'view_saved_locations'), # Saved Locations
    path('account/delete_location/<str:location_id>/', views_account.DeleteSavedLocationView.as_view(), name = 'delete_location'), # Delete Saved Location
    path('account/update_profile_picture/', views_account.UpdateProfilePictureView.as_view(), name = 'update_profile_picture'), # Update Profile Picture

    path('account/calendar/', views_event.CalendarView.as_view(), name = 'calendar'), # Calendar
    path('account/calendar/new/', views_event.EventCreateView.as_view(), name = 'event_new'), # Add Event
    path('account/calendar/all/', views_event.EventListView.as_view(), name = 'event_list'), # Event List
    path('account/calendar/edit/<int:pk>/', views_event.EventUpdateView.as_view(), name = 'event_edit'), # Edit Event
    path('account/calendar/delete/<int:pk>/', views_event.EventDeleteView.as_view(), name = 'event_delete'), # Delete Event
    path('account/calendar/get_locations/', views_event.get_locations, name = 'get_locations'), # Get Locations
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)