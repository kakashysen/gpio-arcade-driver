#!/usr/bin/python

# Import the needed libraries
import RPi.GPIO as GPIO
import time
import thread
from evdev import UInput, ecodes as e

ui = UInput()
GPIO.setwarnings(False)

# This dictionary contains the map for the operative system events, the inputs in
# the GPIO interface for the Raspberry PI 2 and the function state in the arcade machine
#   [FUNCTION] = [PIN, STATE, EVENT]
# When a input signal in the GPIO interface is set to HIGH, the corresponding event is send
# to the operative system and the state is set to true in runtime until the signal is in LOW
interface = {
    "P1_UP": [7, False, e.KEY_W],
    "P1_DOWN": [8, False, e.KEY_S],
    "P1_LEFT": [10, False, e.KEY_A],
    "P1_RIGHT": [11, False, e.KEY_D],
    "P1_A": [15, False, e.KEY_R],
    "P1_B": [16, False, e.KEY_T],
    "P1_C": [21, False, e.KEY_Q],
    "P1_D": [22, False, e.KEY_E],
    "P1_X": [18, False, e.KEY_Y],
    "P1_Y": [19, False, e.KEY_U],
    "P1_SELECT": [13, False, e.KEY_G],
    "P1_START": [12, False, e.KEY_H],
    "P2_UP": [23, False, e.KEY_UP], 
    "P2_DOWN": [24, False, e.KEY_DOWN],
    "P2_LEFT": [26, False, e.KEY_LEFT],
    "P2_RIGHT": [29, False, e.KEY_RIGHT],
    "P2_A": [33, False, e.KEY_4],
    "P2_B": [35, False, e.KEY_5],
    "P2_C": [38, False, e.KEY_0],
    "P2_D": [40, False, e.KEY_3],
    "P2_X": [36, False, e.KEY_1],
    "P2_Y": [37, False, e.KEY_2],
    "P2_SELECT": [32, False, e.KEY_8],
    "P2_START": [31, False, e.KEY_7]
}


# Get all events in the interface
def get_events(item_list): return item_list[2]


# Set the GPIO pin as input with a pull up resistor
def input_setup(item_list):
    print "SETUP GPIO {}".format(item_list[0])
    GPIO.setup(item_list[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    return


# Read the value configured in the interface and emit the corresponding event
def input_read(key, item_list):
    if (not item_list[1]) and (not GPIO.input(item_list[0])):
        item_list[1] = True
        ui.write(e.EV_KEY, item_list[2], 2)
        ui.write(e.EV_KEY, item_list[2], 0)
        ui.syn()
        print "KEY {} PRESS".format(key)
    if item_list[1] and GPIO.input(item_list[0]):
        item_list[1] = False
        ui.write(e.EV_KEY, item_list[2], 1)
        ui.write(e.EV_KEY, item_list[2], 0)
        ui.syn()
        print "KEY {} RELEASE".format(key)
    return


# Set the GPIO to use board pin mode
GPIO.setmode(GPIO.BOARD)

# Set all the used GPIO as inputs with pull up resistor
map(input_setup, interface.values())

# Start main infinite thread for read the inputs and emit the events
try:
    while True:
        for k, v in interface.iteritems():
            thread.start_new_thread(input_read, (k, v))
        time.sleep(0.025)
except KeyboardInterrupt:
    print "BYE"
finally:
    GPIO.cleanup()

