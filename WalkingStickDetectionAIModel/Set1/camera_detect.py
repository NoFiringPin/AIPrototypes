from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
transform=Transform(hflip=1)
picam2.start()
time.sleep(3)
picam2.capture_file("danger.jpg")
print("Image Captured")
