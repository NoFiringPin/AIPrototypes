import firebase_admin
from firebase_admin import credentials, db
from keras.models import load_model
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import board
import neopixel_spi
from plant_monitor import PlantMonitor

# Initialize Firebase Admin SDK
cred = credentials.Certificate("")
firebase_admin.initialize_app(cred, {
    'databaseURL': ''
})

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

pm = PlantMonitor()

# Initialize the camera
pi_camera = Picamera2()
config = pi_camera.create_preview_configuration(main={"format": "RGB888"})
pi_camera.configure(config)
pi_camera.start()
time.sleep(1)

# Initialize LED lights
pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), 50)

monitorValues = [0, 0, 0]  # List to store moisture, temp, and humidity

def update_firebase(moisture, temp, humidity, health_status):
    # Push the updated data to Firebase
    ref = db.reference('plant1')
    ref.update({
        'moisture': str(moisture),
        'temperature': temp,
        'humidity': humidity,
        'healthStatus': health_status,
        'lastWatered': time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())  # optional: update last watered
    })
    print("Firebase updated successfully!")

while True:
    # Capture image from Pi camera
    image = pi_camera.capture_array()
    
    # Resize image for model input
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    # Make prediction using the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Get moisture reading from plant monitor
    monitorValues[0] = pm.get_wetness()
    monitorValues[1] = pm.get_temp()
    monitorValues[2] = pm.get_humidity()

    # Determine plant health status based on moisture
    if monitorValues[0] < 15:
        health_status = "underwatered"
        pixels.fill(0x500000)  # Red light for underwatered
    elif monitorValues[0] < 30:
        health_status = "healthy"
        pixels.fill(0x005000)  # Green light for healthy
    else:
        health_status = "overwatered"
        pixels.fill(0x000050)  # Blue light for overwatered

    # Update Firebase with the new data
    update_firebase(monitorValues[0], monitorValues[1], monitorValues[2], health_status)

    # Print prediction and confidence score
    print(f"Class: {class_name[2:]}, Confidence: {np.round(confidence_score * 100)}%")
    print(f"Moisture: {monitorValues[0]}%, Health Status: {health_status}")

    # Wait for a keypress to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
