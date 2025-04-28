# exec(open("omaha_places_app/scripts/place_categories.py").read())

from omaha_places_app.models import Place
from omaha_places_app.views_venues import PLACE_CATEGORY_MAPPING

updated = 0

for place in Place.objects.all():
    cat_key = place.category.strip()
    if cat_key in PLACE_CATEGORY_MAPPING:
        place.predefined_category = PLACE_CATEGORY_MAPPING[cat_key]
        place.save()
        updated += 1

print(f"Updated {updated} place categories.")