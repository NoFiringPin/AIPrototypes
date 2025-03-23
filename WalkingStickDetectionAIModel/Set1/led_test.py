# Guide
# https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython

# Docs
# https://docs.circuitpython.org/projects/neopixel/en/latest/

# install neopixel
# sudo pip3 install adafruit-circuitpython-neopixel

# Use GPIO pin 12

# for neo pixels to work you must run as a super user
# sudo python led_test.py


import board
import neopixel
import time

# Number of LED to control
num_of_pixels = 10

# The GPIO pin you are using
pixel_pin = board.D12

# Creating the pixel object
pixels = neopixel.NeoPixel(pixel_pin, num_of_pixels, pixel_order = neopixel.GRBW) # Raspberry Pi wiring!, GRBW is inversed actual values are RGBW

brightness = 0.0
# Set the color to the first LED
pixels[0] = (0,0,30,0)

def timed_blinking():
	blink_time = 5
	blink_delay = 0.5
	
	print(blink_time)
	while blink_time > 0:
		pixels[0] = (20,0,0,0)
		time.sleep(blink_delay)
		pixels[0] = (0,0,0,0)
		time.sleep(blink_delay)
		blink_time -= 1
		print(blink_time)
		
def timed_blinking2():
	blink_time = 5
	blink_delay = 0.5
	
	print(blink_time)
	while blink_time > 0:
		pixels[0] = (0,20,0,0)
		time.sleep(blink_delay)
		pixels[0] = (0,0,0,0)
		time.sleep(blink_delay)
		blink_time -= 1
		print(blink_time)
	



# sets the color for all the LEDs
#pixels.fill((255, 0, 0))


timed_blinking()
print('Swapping colors')
time.sleep(1)
timed_blinking2()
pixels.show()
print('done')
