#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SensorCom.py
#
# this program will handle communication
#

import os, serial

#use this space for setting gpio 0 and 1 to '3' only needed on the pcDuino
os.system('echo "3" > /sys/devices/virtual/misc/gpio/modes/gpio0')
os.system('echo "3" > /sys/devices/virtual/misc/gpio/modes/gpio1')

myPort = serial.Serial('/dev/ttyS1', 115200, timeout = 10)

def ingCom():
    myPort.write("e")
    x = myPort.read()
    return x

def indCom():
    myPort.write("f")
    x = myPort.read()
    return x

def bloCom():
    myPort.write("g")
    x = myPort.read()
    return x

if __name__ == __main__:
    print ingCom()
    print indCom()
    print bloCom()

