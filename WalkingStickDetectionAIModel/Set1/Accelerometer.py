import board
import busio
import time
import neopixel
import sys
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)

# Number of LED to control
num_of_pixels = 10

# The GPIO pin you are using
pixel_pin = board.D12

# Creating the pixel object
pixels = neopixel.NeoPixel(pixel_pin, num_of_pixels, pixel_order = neopixel.GRBW) # Raspberry Pi wiring!, GRBW is inversed actual values are RGBW

brightness = 0.0
# Set the color to the first LED
pixels[0] = (0,0,30,0)

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("console_output.txt", "w")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  
    def flush(self):
        pass     
sys.stdout = Logger()

def timed_blinking():
    global program_running
    if accel_z > 10.0:
        print("Over speed")
        pixels[0] = (200,0,0)
        time.sleep(1)
        pixels[0] = (0,0,0)
        time.sleep(1)
        pixels[0] = (200,0,0)
        time.sleep(1)
        pixels[0] = (0,0,0)
        program_running = False
        #with open('console_output.txt', 'w') as f:
        #   f.write("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
        #sys.exit()
    else:
        pixels[0] = (0,0,0,0)
        print("Normal speed")    

program_running = True
while program_running:
    accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
    #velocity_x += accel_x * 0.5
    #velocity_y += accel_y * 0.5
    #velocity_z += accel_z * 0.5
    #print("VX: %0.6f  VY: %0.6f VZ: %0.6f  m/s" % (velocity_x, velocity_y, velocity_z))
    timed_blinking()
    time.sleep(.5)
    
	

    
