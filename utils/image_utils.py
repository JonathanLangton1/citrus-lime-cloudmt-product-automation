from collections import Counter
from PIL import Image
import numpy as np

def find_colour_for_image(image_path):
    # Define the list of predefined colors
    predefined_colors = [
        ('Beige', (245, 245, 220)),
        ('Black', (0, 0, 0)),
        ('Blue', [
            (0, 0, 255),        # Dark blue
            (30, 144, 255),     # Dodger blue
            (0, 191, 255),      # Deep sky blue
            (135, 206, 250),    # Light sky blue
            (176, 224, 230),    # Powder blue
            (240, 248, 255)     # Alice blue
        ]),
        ('Brown', (165, 42, 42)),
        # ('Clear', (255, 255, 255, 0)),
        ('Gold', (255, 215, 0)),
        ('Green', (0, 128, 0)),
        ('Grey', (128, 128, 128)),
        ('Orange', (255, 165, 0)),
        ('Pink', (255, 192, 203)),
        ('Purple', (128, 0, 128)),
        ('Red', (255, 0, 0)),
        ('Silver', (192, 192, 192)),
        ('White', (255, 255, 255)),
        ('Yellow', (255, 255, 0))
    ]

    # Open the image file
    image = Image.open(image_path)

    # Convert the image to RGB mode if it's not already
    image = image.convert('RGB')

    # Calculate the dimensions of the image
    width, height = image.size

    # Calculate the size of the square section to crop
    crop_size = int(min(width, height) * 0.3)

    # Calculate the coordinates for cropping
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size

    # Crop the image to the square section
    image = image.crop((left, top, right, bottom))

    # Resize the image for faster processing if desired
    # image = image.resize((100, 100))

    # Flatten the image array
    pixels = list(image.getdata())

    # Exclude white pixels (RGB values of 255, 255, 255)
    pixels_without_white = [pixel for pixel in pixels if pixel != (255, 255, 255)]

    # Count the occurrence of each color
    color_counts = Counter(pixels_without_white)

    # Get the most frequent color and its count
    most_frequent_color = color_counts.most_common(1)[0][0]

    # Convert RGB to the closest matching predefined color
    def rgb_to_predefined_color(rgb):
        min_distance = float('inf')
        closest_color = None

        for predefined_color, predefined_rgb in predefined_colors:
            # If the predefined color is blue, check for multiple shades
            if predefined_color == 'Blue':
                min_blue_distance = float('inf')
                for shade_rgb in predefined_rgb:
                    distance = np.linalg.norm(np.array(rgb) - np.array(shade_rgb))
                    if distance < min_blue_distance:
                        min_blue_distance = distance
                if min_blue_distance < min_distance:
                    min_distance = min_blue_distance
                    closest_color = predefined_color
            else:
                distance = np.linalg.norm(np.array(rgb) - np.array(predefined_rgb))
                if distance < min_distance:
                    min_distance = distance
                    closest_color = predefined_color

        return closest_color

    # Find the closest matching predefined color
    closest_match = rgb_to_predefined_color(most_frequent_color)

    # print("Most frequent color:", most_frequent_color)
    # print("Closest match:", closest_match)
    return closest_match