import json

import os

from pathlib import Path

import cv2

import google.generativeai as genai

import numpy as np

with open("api_key.json") as f:
    api_key = json.load(f)["api_key"]

genai.configure(api_key=api_key)


def load_image(image_path):
    """Loads an image from file and resizes it to 800x800 pixels."""

    image = cv2.imread(image_path)

    # Resize the image to 800x800 pixels

    image = cv2.resize(image, (800, 800))

    return image


def write_detections(image, food_names):
    """Write the detected food names, bounding boxes, and costs on the image."""

    height, width, _ = image.shape

    # Add a white space to the right side of the image for labels and costs

    white_space_width = 400  # Width of the white space

    white_space = 255 * np.ones((height, white_space_width, 3), np.uint8)

    image = cv2.hconcat([image, white_space])

    # Scale font size and thickness based on image size

    font_scale = min(width, height) / 900

    thickness = max(1, int(font_scale))

    total_cost = 0.0

    y_position = 20  # Initial Y position for the first label

    spacing = 30  # Spacing between labels

    # Header for detected items

    header_text = "Detected Items:"

    cv2.putText(image, header_text, (width + 10, y_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale * 1.2, (0, 0, 255),
                thickness)

    y_position += int(spacing * 1.5)  # Move down for the first item

    for i, food in enumerate(food_names):

        label = food["name"]

        quantity = food["quantity"]

        cost = food.get("cost")

        # Handle cases where cost is None or not a valid number

        if cost is None:

            print(f"Cost for {label} is not available. Defaulting to $0.00.")

            cost = 0.0

        else:

            try:

                cost = float(cost)

            except ValueError:

                print(f"Unable to convert cost for {label}. Skipping...")

                cost = 0.0  # Set to 0 if conversion fails

        total_cost += cost

        bbox = food.get("bounding_box")  # Get bounding box coordinates if available

        # Draw bounding box

        if bbox:
            x, y, w, h = bbox["x"], bbox["y"], bbox["width"], bbox["height"]

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness)

        # Prepare label text

        label_text = f'{label}: {quantity} - ${cost:.2f}'

        cv2.putText(image, label_text, (width + 10, y_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0),
                    thickness)

        y_position += spacing  # Move down for the next item

        # Check if the text fits within the height of the image, and if not, stop adding more text

        if y_position + spacing > height:
            print("Not enough space to draw all labels")

            break

    # Add total cost at the bottom

    total_text = f'Total Cost: ${total_cost:.2f}'

    cv2.putText(image, total_text, (width + 10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale * 1.2, (0, 0, 255),
                thickness)

    return image, total_cost


def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""

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

    # Prompt the model for the food names, portion sizes, and costs in the image

    response = chat_session.send_message(

        "Given this image, identify the food items, their portion sizes, and their costs. "

        "If detecting foods like pizza or burgers identify the whole food and not the individual ingredients"

        "Make sure to include typical market prices for each item in USD. "

        "If the cost is unknown, provide estimated average market prices. "

        "Provide the response as a JSON list with the following format: "

        '[{"name": "<name>", "quantity": <quantity>, "cost": <cost>, '

        '"bounding_box": {"x": <x>, "y": <y>, "width": <width>, "height": <height>}}].'

    )

    response = response.text.replace("```json\n", "").replace('```JSON', '').replace("```", "")

    response = json.loads(response)

    return response


def update_item_counts(item_counts, food_names):
    """Update the item counts based on the detected food names."""

    for food_name in food_names:

        name = food_name["name"]

        quantity = food_name.get("quantity", 1)  # Ensure quantity is available

        if name in item_counts:

            item_counts[name] += quantity

        else:

            item_counts[name] = quantity

    return item_counts


if __name__ == "__main__":

    # Directory containing the images

    image_dir = "."  # Change to '.' to look into the main root directory

    os.makedirs("output", exist_ok=True)

    images = [file for file in os.listdir(image_dir) if file.lower().endswith(('jpg', 'jpeg', 'png'))]

    grand_total_cost = 0.0

    grand_total_items = {}

    for image_file in images:
        filename = Path(image_file).stem

        print(filename)

        image_path = os.path.join(image_dir, image_file)

        food_names = get_food_name_from_image(image_path)

        print(food_names)

        image = load_image(image_path)

        image, total_cost = write_detections(image, food_names)

        # Update grand total cost and items

        grand_total_cost += total_cost

        grand_total_items = update_item_counts(grand_total_items, food_names)

        # Uncomment to show bounding box preview.



        # Show the image in a window

        cv2.imshow(f"Detected Items - {filename}", image)

        cv2.waitKey(0)  # Wait for a key press to close the window



        # Save the image with detections

        output_path = os.path.join(image_dir, 'output', f'{filename}_output.jpg')

        cv2.imwrite(output_path, image)

    # Display the grand total items and cost

    print("\nGrand Total Summary:")

    print(f"Total Cost: ${grand_total_cost:.2f}")

    print("Total Items:")

    for item, count in grand_total_items.items():
        print(f"  {item}: {count}")
