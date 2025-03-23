import board
import neopixel
import time
import cv2
import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path='helmet.pt')

# Create a NeoPixel object
pixels = neopixel.NeoPixel(board.D18, 1)

# Opens image
img = cv2.imread("test.jpg")

# Preprocess the image
img = cv2.resize(img, (416, 416))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = torch.from_numpy(img).float().permute(2, 0, 1) / 255.0
img = img.unsqueeze(0)

# Use the model for prediction
outputs = model(img)
results = outputs.tolist()

# Check if there's a match
if len(results[0]) > 0:
    # If there's a match, blink red
    pixels[0] = (255, 0, 0)
    time.sleep(1)
    pixels[0] = (0, 0, 0)
else:
    # If there's no match, blink green
    pixels[0] = (0, 255, 0)
    time.sleep(1)
    pixels[0] = (0, 0, 0)
