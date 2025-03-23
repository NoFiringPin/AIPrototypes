import cv2
import torch
import os
import time

# Initialize YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Function to detect dangers in "danger.jpg"
def detect_danger_in_image():
    image_path = "/home/pi/danger.jpg"
    while True:
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            results = model(image)
            detections = results.xyxy[0]  # detections in xyxy format
            # Check for close dangers here (assuming danger class id is known, e.g., 'person' is index 0)
            danger_ids = [0]  # example class IDs that are considered dangers
            dangers = any(detection[5].item() in danger_ids and detection[4].item() > 0.5 for detection in detections)  # threshold of 0.5 for confidence
            if dangers:
                image_with_boxes = results.render()[0]
                image = cv2.resize(image_with_boxes, (800,600))
                cv2.putText(image_with_boxes, 'Danger Detected', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                print("Danger Detected")
            else:
                print("No Danger Detected")
                image = cv2.resize(image, (800, 600))
                # If no danger is detected, write "No danger detected" on the image
                cv2.putText(image, 'No danger detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                image_with_boxes = image
            # Resize the imshow window to display the image correctly
            window_name = 'Object Detection'
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 800, 600)  # Resize window to 800x600
            cv2.imshow(window_name, image_with_boxes)
            cv2.waitKey(0)
            # Optionally delete image after processing to avoid reprocessing
            # os.remove(image_path)

        # Short delay before checking for the image again
        time.sleep(0.5)

detect_danger_in_image()
