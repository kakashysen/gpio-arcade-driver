#!/usr/bin/python
import RPi.GPIO as GPIO
import uinput
import time
import thread
from evdev import UInput, ecodes as e

#setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
ui = UInput()

jump=False
up=False
down=False
right=False
left=False

#####################################################################
# List of dictionaries with the controlls configuration
# each dictionary contains the next keys
# <pin_number>, the number of the pin in the GPIO Pi
# <is_pressed>, the boolean value indicate if the button is 
# pressed
# <event_type>, the event type generated when button is pressed
#####################################################################
inputList = [{'pin_number':7, 'is_pressed':False, 'event_type':e.KEY_W},  #P1 UP
             {'pin_number':8, 'is_pressed':False, 'event_type':e.KEY_S},  #P1 DOWN
             {'pin_number':10, 'is_pressed':False, 'event_type':e.KEY_D}, #P1 RIGHT
             {'pin_number':11, 'is_pressed':False, 'event_type':e.KEY_A}, #P1 LEFT
             {'pin_number':12, 'is_pressed':False, 'event_type':e.KEY_H}, #P1 START
             {'pin_number':13, 'is_pressed':False, 'event_type':e.KEY_G}, #P1 SELECT
             {'pin_number':15, 'is_pressed':False, 'event_type':e.KEY_R}, #P1 A
             {'pin_number':16, 'is_pressed':False, 'event_type':e.KEY_T}, #P1 B
             {'pin_number':18, 'is_pressed':False, 'event_type':e.KEY_Y}, #P1 X
             {'pin_number':19, 'is_pressed':False, 'event_type':e.KEY_U}, #P1 Y
             {'pin_number':21, 'is_pressed':False, 'event_type':e.KEY_Q}, #P1 LEFT BOTTOM
             {'pin_number':22, 'is_pressed':False, 'event_type':e.KEY_E}, #P1 RIGHT BOTTOM
             {'pin_number':23, 'is_pressed':False, 'event_type':e.KEY_UP},    #P2 UP
             {'pin_number':24, 'is_pressed':False, 'event_type':e.KEY_DOWN},  #P2 DOWN
             {'pin_number':26, 'is_pressed':False, 'event_type':e.KEY_LEFT},  #P2 LEFT
             {'pin_number':29, 'is_pressed':False, 'event_type':e.KEY_RIGHT}, #P2 RIGHT
             {'pin_number':31, 'is_pressed':False, 'event_type':e.KEY_7},     #P2 START
             {'pin_number':32, 'is_pressed':False, 'event_type':e.KEY_8},     #P2 SELECT
             {'pin_number':33, 'is_pressed':False, 'event_type':e.KEY_4},     #P2 A
             {'pin_number':35, 'is_pressed':False, 'event_type':e.KEY_5},     #P2 B
             {'pin_number':36, 'is_pressed':False, 'event_type':e.KEY_1},     #P2 X
             {'pin_number':37, 'is_pressed':False, 'event_type':e.KEY_2},     #P2 Y
             {'pin_number':38, 'is_pressed':False, 'event_type':e.KEY_0},     #P2 LEFT BOTTOM
             {'pin_number':40, 'is_pressed':False, 'event_type':e.KEY_3},     #P2 RIGHT BOTTOM
	    ]


#####################
# Setup GPIO pins
#####################
def setupGPIO():
  for inputKey in inputList:
    pinNumber = inputKey['pin_number']
    GPIO.setup(pinNumber, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#xcruz#################################
# generate keyboard inputs 
##################################
def keyboardEventsGenerator(inputKey):
  pinNumber = inputKey['pin_number']
  isPressed = inputKey['is_pressed']
  eventType = inputKey['event_type'] 
  if not isPressed and GPIO.input(pinNumber):
    inputKey['is_pressed'] = True
    ui.write(e.EV_KEY, eventType, 2)
    ui.write(e.EV_KEY, eventType, 0)
    ui.syn()
    print "pin {} pressed".format(pinNumber)
  if isPressed and not GPIO.input(pinNumber):
    inputKey['is_pressed'] = False
    ui.write(e.EV_KEY, eventType, 1)
    ui.write(e.EV_KEY, eventType, 0)
    ui.syn()
    print "pin {} release".format(pinNumber)
  return
#####################################################################
# start program
######################################################################## 
setupGPIO()
try:
  while True:
    for inputKey in inputList:
      thread.start_new_thread(keyboardEventsGenerator,(inputKey,))
    time.sleep(0.025)
except:
  print "error keyboars", sys.exc_info()[0]
finally:
  GPIO.cleanup()
