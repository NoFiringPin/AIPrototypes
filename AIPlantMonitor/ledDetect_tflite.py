import tflite_runtime.interpreter as tflite
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import board
import neopixel_spi
from plant_monitor import PlantMonitor

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the TensorFlow Lite model
interpreter = tflite.Interpreter(model_path="plant_model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Initialize Plant Monitor
pm = PlantMonitor()

# Initialize Picamera2
pi_camera = Picamera2()
config = pi_camera.create_preview_configuration(main={"format": "RGB888"})
pi_camera.configure(config)
pi_camera.start()
time.sleep(1)

# Initialize NeoPixel LEDs
pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), 50)

# Initialize monitor readings
monitorValues = [0, 0, 0]

def update_readings():
    while True:
        monitorValues[0] = pm.get_wetness()
        monitorValues[1] = pm.get_temp()
        monitorValues[2] = pm.get_humidity()

while True:
    # Capture image from the camera
    image = pi_camera.capture_array()

    # Resize the image to match model input shape
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Display the captured image
    cv2.imshow("Webcam Image", image)

    # Preprocess the image for the model
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1  # Normalize to [-1, 1]

    # Set the tensor to the model's input tensor
    interpreter.set_tensor(input_details[0]['index'], image)

    # Run inference
    interpreter.invoke()

    # Get the model's output
    output_data = interpreter.get_tensor(output_details[0]['index'])
    index = np.argmax(output_data)
    class_name = class_names[index]
    confidence_score = output_data[0][index]

    # Get monitor readings and control LEDs based on wetness
    monitorValues[0] = pm.get_wetness()
    print(f"{monitorValues[0]}% Moisture")

    if monitorValues[0] < 15:
        pixels.fill(0x500000)  # Red for low moisture
    elif monitorValues[0] < 30:
        pixels.fill(0x005000)  # Green for moderate moisture
    else:
        pixels.fill(0x000050)  # Blue for adequate moisture

    # Print prediction and confidence score
    print(f"{class_name.strip()} ({np.round(confidence_score * 100)}%)")

    # Exit on 'esc' key press
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
