# Ironman Arc Reactor
# This program uses the Circuit Playground Express on the back of a
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

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)
minBrightness = 150
maxBrightness = 240
currentBrightness = minBrightness
step = (maxBrightness - minBrightness)/250
ble_colors = [CYAN[0],CYAN[1],CYAN[2]]

GOING_UP = 0
GOING_DOWN = 1
currentState = GOING_UP

def lin_map(x,xmin,xmax,ymin,ymax):
    return round((ymax-ymin)/(xmax-xmin)*(x-xmin) + ymin)

def updateSystem():
    global currentState
    global currentBrightness

    if(currentState == GOING_UP):
        if(currentBrightness < maxBrightness):
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
    global currentBrightness
    pixels.fill((lin_map(currentBrightness,minBrightness,maxBrightness,0,ble_colors[0]),lin_map(currentBrightness,minBrightness,maxBrightness,0,ble_colors[1]),lin_map(currentBrightness,minBrightness,maxBrightness,0,ble_colors[2])))
    pixels.show()
ble.start_advertising(advertisement)

while True:


    if( ble.connected):
        if uart_service.in_waiting:
            packet = Packet.from_stream(uart_service)
            if isinstance(packet, ColorPacket):
                print(packet.color)
                ble_colors[0] = packet.color[0]
                ble_colors[1] = packet.color[1]
                ble_colors[2] = packet.color[2]

    updateSystem()
    evaluateState()
    reactToState()
    time.sleep(0.0005)
