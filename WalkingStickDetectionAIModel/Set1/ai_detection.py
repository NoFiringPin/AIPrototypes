import cv2
import torch
import os
import time
import buzzer

# Initialize YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Function to detect dangers in "danger.jpg"
def detect_danger_in_image():
    image_path = "/home/pi/danger.jpg"
    output_image_path = "/home/pi/danger_out.jpg"
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
                cv2.putText(image_with_boxes, 'Danger Detected', (100,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 4, cv2.LINE_AA)
                buzzer.beep(2.5,2000)
                print("Danger Detected")
            else:
                print("No Danger Detected")
                image = cv2.resize(image, (800, 600))
                # If no danger is detected, write "No danger detected" on the image
                cv2.putText(image, 'No danger detected', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA)
                image_with_boxes = image
            # Resize the imshow window to display the image correctly
            image = cv2.resize(image_with_boxes, (800,600))
            cv2.imwrite(output_image_path, image)
            window_name = 'Detection Output'
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 800, 600)  # Resize window to 800x600
            cv2.imshow(window_name, image_with_boxes)
            cv2.waitKey(0)
            break
            # Optionally delete image after processing to avoid reprocessing
            # os.remove(image_path)

        # Short delay before checking for the image again
        time.sleep(0.5)
        
detect_danger_in_image()
