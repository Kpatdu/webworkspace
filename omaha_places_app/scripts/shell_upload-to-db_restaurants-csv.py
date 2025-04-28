# DO NOT RUN AS A SCRIPT
# INSTEAD, RUN THE FOLLOWING CODE IN THE SHELL (python manage.py shell):
# THEN, exit() TO EXIT THE SHELL

# OR RUN THE FOLLOWING IN SHELL: exec(open("omaha_places_app/scripts/shell_upload-to-db_restaurants-csv.py").read())

import csv
from omaha_places_app.models import Restaurant

csv_file_path = 'omaha_places_app/cache/new_restaurants.csv'

with open(csv_file_path, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    for row in reader:
        name, address, phone, website, category, price_level, rating, description, image_url = row

        # Convert 'N/A' values to None
        price_level = None if price_level == 'N/A' else price_level
        rating = None if rating == 'N/A' else rating

        # Check if a restaurant with the same name already exists
        existing_restaurant = Restaurant.objects.filter(name=name).first()

        if not existing_restaurant:
            # Create and save restaurant entry
            Restaurant.objects.create(
                name=name,
                address=address,
                category=category,
                price_level=price_level,
                rating=rating,
                description=description,
                website=website,
                phone=phone,
                image=image_url  # Store as CharField if using image URLs
            )
            print(f'Added: {name}')
        else:
            print(f'Skipped (Duplicate): {name}')

print('CSV data imported successfully!')