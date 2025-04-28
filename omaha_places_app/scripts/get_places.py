'''
Modified version of the get_places.py script to grab multiple photos of each location (if available)
'''

import requests
import csv
import time
import os
from dotenv import load_dotenv

# Load Google API key from .env file
dotenv_path = r'omaha_places_app/cache/googleapi.env'
load_dotenv(dotenv_path=dotenv_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Define the location and search parameters
location = '41.2565,-95.9345'  # Omaha, NE coordinates
radius = 10000  # 10km radius
place_types = ['tourist_attraction', 'museum', 'park', 'art_gallery', 'zoo', 'amusement_park', 'library', 'point_of_interest']

MAX_PHOTOS_PER_PLACE = 5  # Change this to get more/less images per place
MIN_PHOTOS_REQUIRED = 1   # Skip locations with fewer than 4 photos


def get_place_details(place_id):
    '''
    Function to fetch additional details using Place Details API
    '''

    details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,website,editorial_summary&key={GOOGLE_API_KEY}'
    response = requests.get(details_url)
    
    if response.status_code == 200:
        details_data = response.json().get('result', {})
        phone = details_data.get('formatted_phone_number', 'N/A')
        website = details_data.get('website', 'N/A')
        description = details_data.get('editorial_summary', {}).get('overview', 'No description available')
        return phone, website, description

    return 'N/A', 'N/A', 'No description available'


def fetch_and_write_to_csv():
    '''
    Function to fetch attractions data and write to CSV, including multiple images.
    '''

    with open('omaha_places_app/cache/new_places.csv', mode = 'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Address', 'Phone', 'Website', 'Category', 'Price Level', 'Rating', 'Description', 'Image URLs'])
        
        for place_type in place_types:
            print(f'Fetching places of type: {place_type}')
            next_page_token = None
            base_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={place_type}&key={GOOGLE_API_KEY}'
            
            while True:
                response = requests.get(base_url if not next_page_token else f'{base_url}&pagetoken={next_page_token}')
                if response.status_code != 200:
                    print(f'Error: Failed to fetch data. Status code: {response.status_code}')
                    return

                data = response.json()
                if 'error_message' in data:
                    print(f'API Error: {data["error_message"]}')
                    return

                places = data.get('results', [])

                # Get places details 
                for place in places:
                    name = place.get('name', 'N/A')
                    address = place.get('vicinity', 'N/A')
                    category = ', '.join(place.get('types', []))
                    price_level = place.get('price_level', 'N/A')  # Fetch price level
                    rating = place.get('rating', 'N/A')

                    # Fetch multiple images if available
                    photos = place.get('photos', [])
                    image_urls = []
                    for photo in photos[:MAX_PHOTOS_PER_PLACE]:  # Get up to MAX_PHOTOS_PER_PLACE
                        image_ref = photo.get('photo_reference')
                        image_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={image_ref}&key={GOOGLE_API_KEY}'
                        image_urls.append(image_url)

                    # Skip adding this place if it has fewer than MIN_PHOTOS_REQUIRED
                    if len(image_urls) < MIN_PHOTOS_REQUIRED:
                        continue

                    image_urls_str = '; '.join(image_urls)

                    # Fetch additional details (phone, website, description)
                    place_id = place.get('place_id', '')
                    phone, website, description = get_place_details(place_id) if place_id else ('N/A', 'N/A', 'No description available')

                    writer.writerow([name, address, phone, website, category, price_level, rating, description, image_urls_str])
                
                print(f'Processed {len(places)} places of type {place_type}.')

                # Check for pagination
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break

                # Avoid hitting API rate limits
                time.sleep(2)

    print('Data written to "places.csv" successfully.')


if __name__ == '__main__':
    fetch_and_write_to_csv()