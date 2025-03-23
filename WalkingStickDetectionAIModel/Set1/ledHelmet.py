import board
import neopixel
import time
import cv2


model = torch.hub.load('ultralytics/yolov5', 'custom', path='helmet.pt')


# Opening image
img = cv2.imread("test.jpg")

# OpenCV opens images as BRG
# but we want it as RGB We'll
# also need a grayscale version
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Don't do anything if there's
# no sign
amount_found = len(found)

def timed_blinking(x, y):
    blink_time = 5
    blink_delay = 0.5
    
    while blink_time > 0:
        pixels[0] = (x, y, 0, 0)
        time.sleep(blink_delay)
        pixels[0] = (0, 0, 0, 0)
        time.sleep(blink_delay)
        blink_time -= 1

while True:
        if len(found) > 0:
                cv2.imshow('image', img_rgb)


                

                num_of_pixels = 7


                # The GPIO pin you are using
                pixel_pin = board.D12

                # Creating the pixel object
                pixels = neopixel.NeoPixel(pixel_pin, num_of_pixels,
                                           pixel_order=neopixel.GRBW)  # Raspberry Pi wiring!, GRBW is inversed actual values are RGBW

                brightness = 0.5
                # Set the color to the first LED
                pixels[0] = (100, 100, 30, 0)
                
                timed_blinking(0, 150)
        else:
                #cv2.imshow('image', img_rgb)

                num_of_pixels = 7

                # The GPIO pin you are using
                pixel_pin = board.D12

                # Creating the pixel object
                pixels = neopixel.NeoPixel(pixel_pin, num_of_pixels,
                                           pixel_order=neopixel.GRBW)  # Raspberry Pi wiring!, GRBW is inversed actual values are RGBW

                brightness = 0.5
                # Set the color to the first LED
                pixels[0] = (100, 100, 30, 0)
                timed_blinking(150, 0)
                
                


        # sets the color for all the LEDs
        # pixels.fill((255, 0, 0))

        # timed_blinking()
        pixels.show()
        print('done')

