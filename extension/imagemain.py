import cv2
import numpy as np
from scipy.stats import entropy
import requests
from io import BytesIO

def calculate_normalized_entropy(image_path):
    # Fetch image from URL
    response = requests.get(image_path)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

    # Read the image from bytes using cv2.imdecode
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

    # Flatten the image into a 1D array
    flat_img = img.flatten()

    # Calculate histogram
    hist, _ = np.histogram(flat_img, bins=256, range=[0, 256])

    # Normalize histogram to get probability distribution
    prob_dist = hist / np.sum(hist)

    # Calculate Shannon's entropy
    entropy_value = entropy(prob_dist, base=2)

    # Normalize entropy to the range [0, 1]
    normalized_entropy = entropy_value / np.log2(len(prob_dist))

    return normalized_entropy

# Example usage
#image_path = 'test5.jpg'
#normalized_entropy_score = calculate_normalized_entropy(image_path)
#print(f"Image Complexity Score: {normalized_entropy_score}")
