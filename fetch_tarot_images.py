import requests
import os
from PIL import Image
import io
from bs4 import BeautifulSoup
import time
import random

# URL patterns
image_base_url = "https://img1.doubanio.com/view/photo/l/public/p{}.webp"
page_base_url = "https://www.douban.com/photos/photo/{}/"

# List of user agents to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
]

# Create a session to maintain cookies
session = requests.Session()

def get_image_name(image_number):
    page_url = page_base_url.format(image_number)
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.douban.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        response = session.get(page_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        descri = soup.find('div', class_='photo_descri')
        if descri:
            return descri.find('div', class_='edtext pl').text.strip()
    except Exception as e:
        print(f"Error fetching image name from {page_url}: {e}")
    return None

def download_image(image_number, retries=3):
    image_url = image_base_url.format(image_number)
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'image/webp,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': page_base_url.format(image_number),
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    for attempt in range(retries):
        try:
            response = session.get(image_url, headers=headers)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return None

# Create TarotCards folder if it doesn't exist
if not os.path.exists("TarotCards"):
    os.makedirs("TarotCards")

# Initial delay
time.sleep(random.uniform(5, 10))

# Download images
image_number = 2377228312
while image_number <= 2377228317:
    image_name = get_image_name(image_number)
    if not image_name:
        image_number += 1
        time.sleep(random.uniform(2, 5))
        continue

    image = download_image(image_number)
    if image:
        # Check if the image is in landscape orientation
        if image.width > image.height:
            print(f"Skipping landscape image from {image_base_url.format(image_number)}")
        else:
            file_name = f"{image_name}.jpg"
            file_path = os.path.join("TarotCards", file_name)
            image.convert("RGB").save(file_path, "JPEG")
            print(f"Downloaded and converted: {file_name}")
    else:
        print(f"Failed to download image for {image_name}")

    image_number += 1
    time.sleep(random.uniform(2, 5))

print("Download and conversion complete!")
