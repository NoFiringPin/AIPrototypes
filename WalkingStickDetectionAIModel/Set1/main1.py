# main.py

import threading
import os
import time
import camera_detect
import ai_detection
import buzzer

# Function to run camera detection
def run_camera_detection():
    camera_detect.camera_detect()

# Function to run AI detection
def run_ai_detection():
    danger_detected = ai_detection.detect_danger_in_image()
    if danger_detected:
        buzzer.beep(1,2000)
    return danger_detected

def main():
    camera_thread = threading.Thread(target=run_camera_detection)
    camera_thread.start()
    
    camera_thread.join()
    danger_detected = run_ai_detection()
    print("Danger detected: ", danger_detected)
