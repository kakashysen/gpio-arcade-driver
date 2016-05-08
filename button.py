import RPi.GPIO as GPIO
import time
from evdev import UInput, ecodes as e

ui = UInput()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    input_state = GPIO.input(11)
    if input_state == True:
        print('Button Pressed')
	ui.write(e.EV_KEY, e.KEY_A, 1)
	ui.write(e.EV_KEY, e.KEY_A, 0)
	ui.syn()
        time.sleep(0.2)
