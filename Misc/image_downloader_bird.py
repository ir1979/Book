import os
import random
import requests
from bs4 import BeautifulSoup

# List of bird types to search for
bird_types = [
    'eagle', 'parrot', 'hummingbird', 'owl', 'penguin',
    'flamingo', 'peacock', 'toucan', 'swan', 'pelican',
    'ostrich', 'woodpecker', 'kingfisher', 'robin', 'bluejay',
    'cardinal', 'sparrow', 'dove', 'pigeon', 'seagull'
]

# Create a directory to store the downloaded images
os.makedirs('bird_images', exist_ok=True)

# Base URL for Google image search
GOOGLE_IMAGE = 'https://www.google.com/search?site=&source=hp&biw=1873&bih=990&tbm=isch&q='

for bird_type in bird_types:
    print(f"Searching for images of {bird_type}...")
    
    # Construct the search URL
    search_url = GOOGLE_IMAGE + bird_type
    
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
            filename = f"{bird_type}_{random.randint(1, 1000000)}.jpg"
            
            # Save the image to the bird_images directory
            with open(f"images/classification/bird/{filename}", 'wb') as f:
                f.write(img_data)
            
            print(f"Downloaded {filename}")
            
            # Limit the number of images downloaded per bird type
            if i >= 20:
                break
        except Exception as e:
            print(f"Could not download image: {e}")
            continue

print("Image download completed.")
