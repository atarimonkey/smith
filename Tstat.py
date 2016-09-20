#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tstat.py
#
# this program will handle monitoring the thermostat
#

import gpio

heat = "gpio2"
heat2 = "gpio3"
cool = "gpio4"
cool2 = "gpio5"
fan = "gpio6"
reversing = "gpio7"

gpio.pinMode(heat, gpio.INPUT)
gpio.pinMode(heat2, gpio.INPUT)
gpio.pinMode(cool, gpio.INPUT)
gpio.pinMode(cool2, gpio.INPUT)
gpio.pinMode(fan, gpio.INPUT)
gpio.pinMode(reversing, gpio.INPUT)

def heat_read():
    stat_w = gpio.digitalRead(heat)
    stat_w2 = gpio.digitalRead(heat2)
    if stat_w == True and stat_w2 != True:
        print "w"
        return "w"
    elif stat_w == True and stat_w2 == True:
        print "w2"
        return "w2"

def cool_read():
    stat_y = gpio.digitalRead(cool)
    stat_y2 = gpio.digitalRead(cool2)
    if stat_y == True and stat_y2 != True:
        print "y"
        return "y"
    elif stat_y == True and stat_y2 == True:
        print "y2"
        return "y2"

def fan_read():
    stat_g = gpio.digitalRead(fan)
    if stat_g == True:
        print "g"
        return "g"

def reversingValve():
    stat_o = gpio.digitalRead(reversing)
    if stat_o == True:
        print "o/b"
        return "o"

def tstatRead():
    tstat = []
    tstat.append(heat_read())
    tstat.append(cool_read())
    tstat.append(fan_read())
    tstat.append(reversingValve())
    return tstat

if __name__ == '__main__':
    print tstatRead()

