#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# senscom.py
#
# this program will handle communication
#

import os, serial, bme280

#use this space for setting gpio 0 and 1 to '3' only needed on the pcDuino
os.system('echo "3" > /sys/devices/virtual/misc/gpio/modes/gpio0')
os.system('echo "3" > /sys/devices/virtual/misc/gpio/modes/gpio1')

si2cadd = #i2c address for the supply sensor
sbus = # bus for the supply sensor
ri2cadd = # i2c address for the return sensor
rbus = #bus for the return sensor
sbme = bme280.BME280(sbus, si2cadd) 
rbme = bme280.BME280(rbus, ri2cadd)


def inducer():
        x = float(comm('f'))
        return x

def flame():
	x = comm('e')
    if x == '1' or 'True':
		return True
    else:
        return False

def blower():
	x = float(comm('g'))
    return x

def temp_rise():
        deltaT = supplyTemp() - returnTemp()
        return deltaT

def temp_drop():
	deltaT = returnTemp() - supplyTemp()
	return deltaT

def delta_h():
	d = returnHumid() - supplyHumid()
	return d

def delta_e():
	e = entholpy(returnTemp(), returnHumid()) - entholpy(supplyTemp(), supplyHumid())
    return e

def capacity(cfm):
	cap = delta_e() * 4.5 * cfm
    return cap

def entholpy(temp, humid):
	t = temp + 459.67
	n = math.log(t)
    l = -10440.4 / t - 11.29465 - 0.02702235 * t + 0.00001289036 * t ** 2 - 0.000000002478068 * t ** 3 + 6.545967 * n
    s = math.exp(l)
    p = humid / 100 * s
    w = 0.62198 * p / (14.7 - p)
    h = 0.24 * temp + w * (1061 + 0.444 * temp)
    return h

def returnTemp():
	x = rbme.readData('t')
    return x

def returnHumid():
	x = rbme.readData('h')
    return x

def returnPress():
	x = rbme.readData('p')
	return x

def supplyTemp():
	x = sbme.readData('t')
    return x

def supplyHumid():
	x = sbme.readData('h')
    return x

def supplyPress():
	x = sbme.readData('p')
	return x

def comm(z):
	# handles the communication
    myPort = serial.Serial('/dev/ttyS1', self.comm_speed, timeout = 10)
    myPort.write(z)
    x = myPort.readline()
    myPort.close()
    return x


if __name__ == __main__:
    print supplyTemp()
    print returnTemp()
    print supplyHumid()
    print returnHumid()
    print blower()
    print inducer()
    print flame()

