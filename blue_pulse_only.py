# Ironman Arc Reactor
# This program uses the Circuit Playground Bluefruit to pulse Neopixels and make a slow, pulsing cyan glow as part of an Arc reactor prop.
# Programmed by Evan Weinberg in CircuitPython

import time
import board
import neopixel

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.9, auto_write=False)
minBrightness = 50
maxBrightness = 250
currentBrightness = minBrightness
step = (maxBrightness - minBrightness)/100

GOING_UP = 0
GOING_DOWN = 1
currentState = GOING_UP

def updateSystem():
    global currentState
    global currentBrightness

    if(currentState == GOING_UP):
        if(currentBrightness <= maxBrightness):
            currentBrightness += step
        else:
            currentState = GOING_DOWN
    else:
        if(currentBrightness>minBrightness):
            currentBrightness -= step
        else:
            currentState = GOING_UP

def evaluateState():
    global currentState
    global currentBrightness
    if(currentState == GOING_UP):
        if(currentBrightness > maxBrightness):
            currentState = GOING_DOWN
    else:
        if(currentBrightness<minBrightness):
            currentState = GOING_UP

def reactToState():
    pixels.fill((0,round(currentBrightness),round(currentBrightness)))
    pixels.show()

while True:
    updateSystem()
    evaluateState()
    reactToState()
    time.sleep(0.01)
