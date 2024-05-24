import os
import random
import requests
from bs4 import BeautifulSoup

# List of butterfly types to search for
butterfly_types = [
    'monarch butterfly', 'swallowtail butterfly', 'blue morpho butterfly', 'peacock butterfly', 'painted lady butterfly',
    'red admiral butterfly', 'common buckeye butterfly', 'zebra longwing butterfly', 'tiger swallowtail butterfly', 'question mark butterfly',
    'great spangled fritillary butterfly', 'mourning cloak butterfly', 'viceroy butterfly', 'pipevine swallowtail butterfly', 'spicebush swallowtail butterfly',
    'black swallowtail butterfly', 'eastern tiger swallowtail butterfly', 'giant swallowtail butterfly', 'two-tailed swallowtail butterfly', 'luna moth'
]


# Base URL for Google image search
GOOGLE_IMAGE = 'https://www.google.com/search?site=&source=hp&biw=1873&bih=990&tbm=isch&q='

for butterfly_type in butterfly_types:
    print(f"Searching for images of {butterfly_type}...")
    
    # Construct the search URL
    search_url = GOOGLE_IMAGE + butterfly_type
    
    # Send a GET request to the search URL
    response = requests.get(search_url)
    
    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <img> tags
    img_tags = soup.find_all('img')
    
    # Download and save the images
    for i, img_tag in enumerate(img_tags):
        try:
            # Get the image URL
            img_url = img_tag['src']
            
            # Send a GET request to the image URL
            img_data = requests.get(img_url).content
            
            # Generate a random filename for the image
            filename = f"{butterfly_type.replace(' ', '_')}_{random.randint(1, 1000000)}.jpg"
            
            # Save the image to the butterfly_images directory
            with open(f"images/classification/butterfly/{filename}", 'wb') as f:
                f.write(img_data)
            
            print(f"Downloaded {filename}")
            
            # Limit the number of images downloaded per butterfly type
            if i >= 20:
                break
        except Exception as e:
            print(f"Could not download image: {e}")
            continue

print("Image download completed.")
