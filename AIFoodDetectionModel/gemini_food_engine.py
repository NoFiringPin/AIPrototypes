"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""
import csv
import json
import os
from pathlib import Path

import cv2
import google.generativeai as genai
import numpy as np

with open("api_key.json") as f:
    api_key = json.load(f)["api_key"]

genai.configure(api_key=api_key)

with open("labelmap.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]


def load_item_prices_from_csv(csv_file_path):
    """Load item prices from a CSV file."""
    item_prices = {}
    with open(csv_file_path, mode='r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            item = row['item']
            price = float(row['price'])
            item_prices[item] = price
    return item_prices


def load_image(image_path):
    """Loads an image from file."""
    image = cv2.imread(image_path)
    return image


def write_detections(image, food_names):
    """Write the detected food names on the image."""

    height, width, _ = image.shape
    # Concatenate a white image to the right side of the original image
    white_space_width = 400  # Width of the white space
    white_space = 255 * np.ones((height, white_space_width, 3), np.uint8)
    image = cv2.hconcat([image, white_space])

    # Scale the font size based on image dimensions
    font_scale = min(width, height) / 700
    thickness = max(1, int(font_scale))

    for i, food in enumerate(food_names):
        label = food["name"]
        quantity = food["quantity"]
        # Draw label
        label_text = f'{label}: {quantity}'
        (text_width, text_height), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                                                              thickness)
        # Adjust the spacing between labels
        spacing = 20  # Additional spacing between labels

        # Calculate the y-coordinate for the current text
        y_position = 10 + (i + 1) * (text_height + spacing)

        # Check if the text fits within the height of the image, and if not, stop adding more text
        if y_position + text_height > height:
            print("Not enough space to draw all labels")
            break

        # Write the label on the white image (right side of the original image)
        cv2.putText(image, label_text, (width + 10, y_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0),
                    thickness)

    return image


def calculate_total_cost(item_counts, item_prices):
    """Calculate the total cost of detected items."""
    total_cost = 0.0
    for item, count in item_counts.items():
        if item in item_prices:
            total_cost += item_prices[item] * count
    return total_cost


def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


def create_gemini_model(model_name):
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    return model


def get_food_name_from_image(image_path):
    # Upload the image to Gemini
    image_file = upload_to_gemini(image_path, mime_type="image/jpeg")

    # Start a chat session with the model
    model = create_gemini_model("gemini-1.5-flash")
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    image_file,
                ],
            },
        ]
    )

    # Prompt the model for the food names in the image
    response = chat_session.send_message(
        f"Giving this image, tell me what are the food name that are in there from this list: {labels}. Write the "
        'response as a json that looks like this: '
        '[{"name":<name>,"quantity":<quantity in int>]. '
        'If there is sandwich do not write bread'
    )

    response = response.text.replace("```json\n", "").replace('```JSON', '').replace("```", "")
    response = json.loads(response)
    return response


def update_item_counts(item_counts, food_names):
    """Update the item counts based on the detected food names."""
    for food_name in food_names:
        name = food_name["name"]
        if name in item_counts:
            item_counts[name] += food_name["quantity"]
    return item_counts


if __name__ == "__main__":
    # Load item prices from CSV
    os.makedirs("output", exist_ok=True)
    item_prices = load_item_prices_from_csv("all_foods.csv")
    # Directory containing the images
    image_dir = "."  # change to '.' to look into the main root directory
    images = [file for file in os.listdir(image_dir) if file.lower().endswith(('jpg', 'jpeg', 'png'))]

    total_item_counts = {item: 0 for item in labels}

    for image_file in images:
        filename = Path(image_file).stem
        print(filename)
        item_counts = {item: 0 for item in labels}
        image_path = os.path.join(image_dir, image_file)
        food_names = get_food_name_from_image(image_path)
        print(food_names)
        item_counts = update_item_counts(item_counts, food_names)
        image = load_image(image_path)
        image = write_detections(image, food_names)
        output_path = os.path.join(image_dir, 'output', f'{filename}_output.jpg')
        cv2.imwrite(output_path, image)
        total_cost = calculate_total_cost(item_counts, item_prices)
        total_item_counts = update_item_counts(total_item_counts, food_names)
        print(f"Detected items in {image_file}: {food_names}")
        print(f"Total cost of detected items in {image_file}: ${total_cost:.2f}")

    grand_total = calculate_total_cost(total_item_counts, item_prices)
    print(f"Grand Total item counts: {total_item_counts}")
    print(f"Grant Total Cost:${grand_total:.2f}")
