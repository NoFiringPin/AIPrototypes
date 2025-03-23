import board
import busio
import time
import adafruit_vl6180x

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)

while True: 
    range_mm = sensor.range
    print("Range: {0}mm".format(range_mm))
    time.sleep(1)
