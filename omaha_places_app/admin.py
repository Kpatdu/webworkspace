from django.contrib import admin
from django.db import models
from omaha_places_app.models import Restaurant, Place

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'website', 'category', 'price_level', 'rating')
    list_filter = ('category', 'price_level', 'rating')
    search_fields = ('name', 'address', 'phone',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'website', 'category', 'price_level', 'rating')
    list_filter = ('category', 'price_level', 'rating')
    search_fields = ('name', 'address', 'phone',)