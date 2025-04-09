from django.contrib import admin
from .models import Restaurant, Place, Comment

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
    list_display = ('user', 'place', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user', 'place', 'text',)