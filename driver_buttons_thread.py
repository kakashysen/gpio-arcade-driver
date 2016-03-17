#!/usr/bin/python
import RPi.GPIO as GPIO
import uinput
import time
from evdev import UInput, ecodes as e
import threading

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, delay):
        #setup GPIUO using Board numbering
        GPIO.setmode(GPIO.BOARD)

        # Player 1
	if name == "jump":
	  GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #fire P1
	if name == "right":
	  GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #right P1
	if name == "left":
	  GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #left P1
        
	threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
    def run(self):
        print "Starting " + self.name
	# Player 1
        if self.name == "jump":
          GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #fire P1
	  jumpFunction(self.name, self.counter)
        if self.name == "right":
          GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #right P1
	  rightFunction(self.name, self.counter)
        if self.name == "left":
          GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #left P1
          leftFunction(self.name, self.counter)
        print "Exiting " + self.name

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

# Create new threads
delay=0.01
thread1 = myThread(1, "jump", delay)
thread2 = myThread(2, "right", delay)
thread3 = myThread(3, "left", delay)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()


print "Exiting Main Thread"
