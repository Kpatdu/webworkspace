from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
#comment imports

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

'''
To delete items from the database
in the terminal: 
python manage.py shell
and paste one of the following:

### Option 1: Delte all objects from the database ###

from omaha_places_app.models import Restaurant, Place, Comment

# Delete all restaurants (be careful with this!)
Comment.objects.all().delete()
Restaurant.objects.all().delete()
Place.objects.all().delete()


### Alternatively: ###

from omaha_places_app.models import Restaurant, Place

# Delete a specific restaurant by primary key (ID)
restaurant = Restaurant.objects.get(id=ID)
restaurant.delete()
'''


class Restaurant(models.Model):
    '''
    Model for manually adding a restaurant page.
    '''

    name = models.CharField('Restaurant Name', help_text = 'Name of the restaurant', max_length = 100)
    address = models.CharField('Address', help_text = 'Restaurant address', max_length = 100)
    phone = models.CharField('Phone', help_text = 'Phone number', max_length = 20)
    website = models.URLField('Website', help_text = 'Website URL')
    category = models.CharField('Category', help_text = 'Category of the restaurant', max_length = 50)

    predefined_category = models.CharField('Predefined Category',help_text='restaurant category', max_length=50, blank=True, null=True)

    price_level = models.CharField('Price Level', help_text = 'Price level of the restaurant', max_length = 50, blank = True, null =  True)
    rating = models.DecimalField('Rating', help_text = 'Rating of the restaurant', max_digits = 2, decimal_places = 1, blank = True, null = True)
    description = models.TextField('Description', help_text = 'Restaurant description')
    image = models.ImageField('Image', help_text = 'Image of the restaurant', upload_to = 'images/')

    class Meta():
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name


class Place(models.Model):
    '''
    Model for manually adding a place page.
    '''
    
    name = models.CharField('Place Name', help_text = 'Name of the place', max_length = 100)
    address = models.CharField('Address', help_text = 'Place address', max_length = 100)
    phone = models.CharField('Phone', help_text = 'Phone number', max_length = 20)
    website = models.URLField('Website', help_text = 'Website URL')
    category = models.CharField('Category', help_text = 'Category of the place', max_length = 50)

    predefined_category = models.CharField('Predefined Category',help_text='place category', max_length = 50, blank=True, null=True)

    price_level = models.CharField('Price Level', help_text = 'Price level of the restaurant', max_length = 50, blank = True, null =  True)
    rating = models.DecimalField('Rating', help_text = 'Rating of the restaurant', max_digits = 2, decimal_places = 1, blank = True, null = True)
    description = models.TextField('Description', help_text = 'Place description')
    image = models.ImageField('Image', help_text = 'Image of the place', upload_to = 'images/')

    class Meta():
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    '''
    Model for adding comments on a restaurant or place.
    '''

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.user}"
    