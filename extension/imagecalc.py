from bs4 import BeautifulSoup
import requests
import imagemain as im

def calculate_image(url):
    try:
        image_complexity = 0
        # Fetch the HTML content of the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags
        img_tags = soup.find_all('img')
        num_images = len(img_tags)

        for img_tag in img_tags:
            # Extract image URL from the img tag
            img_url = img_tag.get('src', '')
            image_complexity += im.calculate_normalized_entropy(url + img_url)

        # Calculate average image complexity
        if num_images > 0:
            return image_complexity / num_images
        else:
            return 0  # To avoid division by zero if there are no images

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
