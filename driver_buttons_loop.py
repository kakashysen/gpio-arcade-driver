#!/usr/bin/python
import RPi.GPIO as GPIO
import uinput
import time
import thread
from evdev import UInput, ecodes as e

#setup GPIUO using Board numbering
GPIO.setmode(GPIO.BOARD)

ui = UInput()

# Player 1
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #fire P1
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  #up P1
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #down P1
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #right P1
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #left P1

# add event for fire button
GPIO.add_event_detect(11, GPIO.RISING, bouncetime=200)

jump=False
up=False
down=False
right=False
left=False

device = uinput.Device([
  uinput.KEY_A,
  uinput.KEY_B,
  uinput.ABS_X,
  uinput.ABS_Y,
  ])


inputList = [{'channel':7, 'active':False, 'input_type':uinput.ABS_Y,'center_value':128, 'move_value':0},
             {'channel':13, 'active':False, 'input_type':uinput.ABS_Y,'center_value':128, 'move_value':255},
             {'channel':15, 'active':False, 'input_type':uinput.ABS_X,'center_value':128, 'move_value':255},
             {'channel':16, 'active':False, 'input_type':uinput.ABS_X,'center_value':128, 'move_value':0}]

def jumpFunction(threadName, delay):
  jump=False
  while True:
    if GPIO.input(11):
      jump=True
      with UInput() as ui:
        ui.write(e.EV_KEY, e.KEY_A, 2)
        ui.syn()
      print("jump")
    elif jump and not GPIO.input(11):
      jump=False
      with UInput() as ui:
        ui.write(e.EV_KEY, e.KEY_A, 1)
        ui.syn()
      print("stop jump")
    time.sleep(delay)

def rightFunction(threadName, delay):
  right=False
  while True:
    if GPIO.input(15):
      right=True
      with UInput() as ui:
        ui.write(e.EV_KEY, e.KEY_RIGHT, 2)
        ui.syn()
      print("rigth")
    elif right and not GPIO.input(15):
      right=False
      with UInput() as ui:
        ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
        ui.syn()
      print("stop right")
    time.sleep(delay)

def leftFunction(threadName, delay):
  left=False
  while True:
    if GPIO.input(16):
      left=True
      with UInput() as ui:
        ui.write(e.EV_KEY, e.KEY_LEFT, 2)
        ui.syn()
      print("left")
    elif left and not GPIO.input(16):
      left=False
      with UInput() as ui:
        ui.write(e.EV_KEY, e.KEY_LEFT, 1)
        ui.syn()
      print("stop left")
    time.sleep(delay)

while True:
  if GPIO.input(15):
    right=True
    ui.write(e.EV_KEY, e.KEY_RIGHT, 2)
    ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
    ui.syn()
    print("rigth")
  elif right and not GPIO.input(15):
    right=False
    ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
    ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
    ui.syn()
    print("stop right")
 
  if GPIO.input(16):
    left=True
    ui.write(e.EV_KEY, e.KEY_LEFT, 2)
    ui.write(e.EV_KEY, e.KEY_LEFT, 0)
    ui.syn()
    print("left")
  elif left and not GPIO.input(16):
    left=False
    ui.write(e.EV_KEY, e.KEY_LEFT, 1)
    ui.write(e.EV_KEY, e.KEY_LEFT, 0)
    ui.syn()
    print("stop left")
    
  if GPIO.input(11):
    jump=True
    ui.write(e.EV_KEY, e.KEY_A, 2)
    ui.write(e.EV_KEY, e.KEY_A, 0)
    ui.syn()
    print("jump")
  elif jump and not GPIO.input(11):
    jump=False
    ui.write(e.EV_KEY, e.KEY_A, 1)
    ui.write(e.EV_KEY, e.KEY_A, 0)
    ui.syn()
    print("stop jump")

  time.sleep(0.025)
GPIO.cleanup()
