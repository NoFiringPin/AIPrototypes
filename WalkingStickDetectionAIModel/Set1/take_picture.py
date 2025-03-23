#imports

import cv2
from picamera2 import Picamera2
import time

# Initialize the pi camera
pi_camera = Picamera2()

# Set color mode to RGB
config = pi_camera.create_preview_configuration(main={"format": "RGB888"})

pi_camera.configure(config)

# start the picamera and let it set up

pi_camera.start()
print('preparing camera...')
time.sleep(3)

image = pi_camera.capture_array()

# flip the image

# image = cv2.flip(image, -1)
cv2.imwrite('capture.jpg', image)

print('image captured')
