import cv2
from picamera2.picamera2 import Picamera2
import numpy as np
import torch
import RPi.GPIO as GPIO
import time

# Buzzer setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

def beep(duration=0.5, frequency=1000):
    cycle_time = 1.0 / frequency
    on_time = cycle_time / 2
    off_time = cycle_time / 2
    start_time = time.time()
    while (time.time() - start_time) < duration:
        GPIO.output(13, GPIO.HIGH)
        time.sleep(on_time)
        GPIO.output(13, GPIO.LOW)
        time.sleep(off_time)

# Initialize YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Function to detect dangers in the captured image
def detect_danger(image):
  results = model(image)
  detections = results.xyxy[0]  # detections in xyxy format
  danger_ids = [0]  # example class IDS that are considered dangers
  dangers = any(
      detection[5].item() in danger_ids and detection[4].item() > 0.5
      for detection in detections)
  return dangers

# Capture an image using Picamera2
def capture_image():
    picam2 = Picamera2()
    config = picam2.preview_configuration(main={"size":(640, 480)})
    picam2.configure(config)
    picam2.start()
    time.sleep(2)  # Warm-up time
    image_array = picam2.capture_array()
    picam2.stop()
    return image_array

def main():
    # Capture an image
    image_array = capture_image()
    # Convert the captured image for YOLOv5
    img_for_yolo = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    # Detect danger
    if detect_danger(img_for_yolo):
        print("Danger Detected! Alerting with buzzer.")
        beep()  # Use the buzzer to alert
    else:
        print("No Danger Detected.")

if __name__ == "__main__":
    main()
    GPIO.cleanup()
