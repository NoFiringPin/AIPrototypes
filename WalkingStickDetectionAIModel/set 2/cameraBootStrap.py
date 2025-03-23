import cv2
from picamera2 import Picamera2
import time

pi_camera = Picamera2()
config = pi_camera.create_preview_configuration(main={"format": "RGB888"})
pi_camera.configure(config)

pi_camera.start()
time.sleep(1)

while True:
    image = pi_camera.capture_array() 
    cv2.imshow("Camera 1", image)

    if cv2.waitKey(0):
        break

cv2.destroyAllWindows

print("Done")
