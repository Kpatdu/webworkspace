# exec(open("omaha_places_app/scripts/restaurant_categories.py").read())

from omaha_places_app.models import Restaurant
from omaha_places_app.views_venues import RESTAURANT_CATEGORY_MAPPING
updated = 0

for restaurant in Restaurant.objects.all():
    cat_key = restaurant.category.strip()
    if cat_key in RESTAURANT_CATEGORY_MAPPING:
        restaurant.predefined_category = RESTAURANT_CATEGORY_MAPPING[cat_key]
        restaurant.save()
        updated += 1

print(f"Updated {updated} restaurant categories.")