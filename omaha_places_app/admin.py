from django.contrib import admin
from .models import Restaurant, Place, Comment, Event, SavedLocation

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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'restaurant', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user', 'place', 'restaurant', 'text',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'start_time', 'end_time', 'get_location_name')
    list_filter = ('user', 'name', 'start_time', 'end_time',)
    search_fields = ('user', 'name', 'start_time', 'end_time',)

    def get_location_name(self, obj):
        return str(obj.location) if obj.location else 'N/A'
    get_location_name.short_description = 'Location'

@admin.register(SavedLocation)
class SavedLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'location_id', 'location_type',)
    list_filter = ('user', 'name')
    search_fields = ('user', 'name', 'location_id', 'location_type')
