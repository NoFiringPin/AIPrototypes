import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(13, GPIO.OUT)  # Set pin 33 (GPIO 13) to be an output pin


def beep(duration, frequency):
  """
    Generates a beep sound in the buzzer.
    :param duration: Duration of the beep in seconds.
    :param frequency: Frequency of the beep
    """
  cycle_time = 1.0 / frequency
  on_time = cycle_time / 2
  off_time = cycle_time /2
  
  start_time = time.time()
  while (time.time() - start_time) < duration:
    GPIO.output(13, GPIO.HIGH)  # Turn on buzzer
    time.sleep(on_time)
    GPIO.output(13, GPIO.LOW)  # Turn off buzzer
    time.sleep(off_time)


# Example usage
if __name__ == "__main__":
  try:
    while True:
      beep(0.5, 2000)  # Beep for 0.5 seconds
      time.sleep(1)  # Wait for 1 second between beeps
  except KeyboardInterrupt:
    print("Program exited by user")
  finally:
    GPIO.cleanup(
    )  # Clean up GPIO to reset any resources that have been allocated.
