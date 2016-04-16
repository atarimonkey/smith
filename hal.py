#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2009 Unknown <ubuntu@ubuntu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import smbus
import math
import time
import pingo
import log
import json

settings = []
#class Check():
board = pingo.detect.MyBoard()

#led_pin = board.pins[13]
#led_pin.mode = pingo.OUT

# this sets the fan out pin
g_out = board.pins[5]
g_out.mode = pingo.OUT

# this sets the cooling out pin
y_out = board.pins[3]
y_out.mode = pingo.OUT

# this sets the heat out pin
w_out = board.pins[7]
w_out.mode = pingo.OUT

# this sets the fan pin
g_in = board.pins[4]
g_in.mode = pingo.IN

# this sets the cooling pin
y_in = board.pins[2]
y_in.mode = pingo.IN

#this sets the heat pin
w_in = board.pins[6]
w_in.mode = pingo.IN

# this sets the second stage heat pin 
w_two_in = board.pins[8]
w_two_in.mode = pingo.IN

inducerAmps = 0.0
blowerAmps = 0.0
deltaT = 0
deltaE = 0.0
avg = 0

    
#    def __init__(self, heat_stages, timed,  cool_stages, hp, furnace_type, comm_speed):
#        self.h_stages = heat_stages
#        self.c_stages = cool_stages
#        self.hp = hp
#        self.f_type = furnace_type
#        self.comm_speed = comm_speed
#        self.timed = timed
        
def w_read():
        # this will read the the heat terminal
        if w_in.state == 'LOW':
                return True
        
        else:
                return False
                
def w_two_read():
        # this will read the second stage heat terminal
        if w_two_in.state == 'LOW':
                return True
                
        else:
                return False
                
def y_read():
        # this will read the cooling terminal
        if y_in.state == 'LOW':
                return True
                
        else:
                return False
                
def g_read():
        # this will read the fan termanal
        if g_in.state == 'LOW':
                return True
                
        else:
                return False

# setup the equipment
# take the info given and create a list of equipment
def heat_call(start_time,f, h_stages, timed):
        start = start_time
        global blowerAmps
        global inducerAmps
        global deltaT
        global avg
        if f == "furnace" or "gas" or "Furnace" or "Gas":
                if h_stages == '2' and timed:
                        w_out.lo()
                        if heat_start(start):
                                current_time = time.ctime()
                                while (current_time - start) < (9*60) and w_read():
                                        heat_stage_one(start)
                                        time.sleep(1)
                                        current_time = time.ctime()
                                while w_read():
                                        heat_stage_two(start)
                                w_out.hi()
                                blowerAmps = blowerAmps / avg
                                inducerAmps = inducerAmps / avg
                                deltaT = deltaT / avg
                                c = time.ctime()
                                log.entry('furnace', c - start, blowerAmps, inducerAmps, deltaT, 0.0)
                                return
                        else:
                                w_out.hi()
                                return 

                elif h_stages == '2' and timed == False:
                        w_out.lo()
                        if heat_start(start):
                                time.sleep(1)
                                while w_read():
                                        heat_stage_one(start)
                                        while w_two_read():
                                                w2('on')
                                                heat_stage_two(start)
                                w2('off')
                                w_out.hi()
                                blowerAmps = blowerAmps / avg
                                inducerAmps = inducerAmps / avg
                                deltaT = deltaT / avg
                                c = time.ctime()
                                log.entry('furnace', c - start, blowerAmps, inducerAmps, deltaT, 0.0)
                                return
                        
                        else:
                                w_out.hi()
                                return
                        

                else:
                        w_out.lo()
                        if heat_start(start):
                                time.sleep(30)
                                while w_read():
                                        heat_stage_two(start)
                        w_out.hi()
                        blowerAmps = blowerAmps / avg
                        inducerAmps = inducerAmps / avg
                        deltaT = deltaT / avg
                        c = time.ctime()
                        log.entry('furnace', c - start, blowerAmps, inducerAmps, deltaT, 0.0)
                        return
                                

        elif f_type == "air handler with heat strips":
                w_out.lo()
                while w_read():
                        air_handler_heat_strips(start)
                        time.sleep(1)
                w_out.hi()
                blowerAmps = blowerAmps / avg
                inducerAmps = inducerAmps / avg
                deltaT = deltaT / avg
                c = time.ctime()
                log.entry('furnace', c - start, blowerAmps, inducerAmps, deltaT, 0.0)
                return

# start the furnace
def heat_start(startTime):
        global settings
        global avg
        global inducerAmps
        global blowerAmps
        global deltaT
        s = startTime
        c = time.ctime
        avg = avg + 1
        if inducer() > 0:
                inducerAmps = inducerAmps + inducer()
                time.sleep(30)
#                f = 0
#                p = 0
#        
#                while p < 3:
#                        if p == 0 and flame():
#                                f = 1
#                                p += 1
#                                time.sleep(2)
#                                return
#
#                        elif p == 0 and not flame():
#                                p += 1
#                                time.sleep(2)
#                                return
#
#                        elif p > 0 and f == 0:
#                                if not flame():
#                                        p += 1
#                                        time.sleep(2)
#                                        return
#
#                                else:
#                                        f = 1
#                                        p += 1
#                                        time.sleep(2)
#                                        return
#
#                        elif p > 0 and f == 1:
#                                p += 1
#                                time.sleep(2)
#                                return
#
#                if flame():
                if start_up_flame_sensor_test(s):
                        b = 0
                        while blower() == 0:
                                if b >= 123:
                                        blowerAmps = blowerAmps + blower()
                                        deltaT = deltaT + temp_rise()
                                        c = time.ctime()
                                        log.error('furnace', 'blower', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_blower(settings[1], settings[3], settings[4]))
                                        return False

                                else:
                                        time.sleep(1)
                                        b +=1
                                        return

                        if 2.5 < blower() > 10:
                                blowerAmps = blowerAmps + blower()
                                return True

                        else:
                                blowerAmps = blowerAmps + blower()
                                deltaT = deltaT + temp_rise()
                                c = time.ctime()
                                log.error('furnace', 'blower amps', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_blower(settings[1], settings[3], settings[4]))
                                return False

#                elif f == 0 and not flame():
#                        blowerAmps = blowerAmps + blower()
#                        deltaT = deltaT + temp_rise()
#                        c = time.ctime()
#                        log.error('furnace', 'ignition', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_ignition(settings[1], settings[3], settings[4]))
#                        return False
#
#                elif f == 1 and not flame():
#                        blowerAmps = blowerAmps + blower()
#                        deltaT = deltaT + temp_rise()
#                        c = time.ctime()
#                        log.error('furnace', 'flame sensor', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_flame_sensor(settings[1], settings[3], settings[4]))
#                        return False
#
#                else:
#                        blowerAmps = blowerAmps + blower()
#                        deltaT = deltaT + temp_rise()
#                        c = time.ctime()
#                        log.error('furnace', 'ignition', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_ignition(settings[1], settings[3], settings[4]))
#                        return False

# new flame sensor test
def start_up_flame_sensor_test(start_time, ):
        global settings
        global inducerAmps
        global blowerAmps
        global deltaT
        s = start_time
        ign = 0
        if flame() == 'True' or flame() == True:
                ign = ign + 1
        time.sleep(4)
        if flame() == 'False' or flame() == False:
                if ign == 0:
                        blowerAmps = blowerAmps + blower()
                        deltaT = deltaT + temp_rise()
                        c = time.ctime()
                        log.error('furnace', 'ignition', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_ignition(settings[1], settings[3], settings[4]))
                        return False
                elif ign == 1:
c                        blowerAmps = blowerAmps + blower()
                        deltaT = deltaT + temp_rise()
                        c = time.ctime()
                        log.error('furnace', 'flame sensor', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_flame_sensor(settings[1], settings[3], settings[4]))
                        return False
        elif flame() == 'True' or flame() == True:
                return True
        
# furnace stage 1
def heat_stage_one(start_time):
        global settings
        global avg
        avg = avg + 1
        global blowerAmps
        global inducerAmps
        global deltaT
        s = start_time
        c = time.ctime()
        if 0.0 < inducer() < 1.0:
                inducerAmps = inducerAmps + inducer()

                if flame():
                        if 2.5 < blower() < 10:
                                blowerAmps = blowerAmps + blower()
                                c = time.ctime()
                                if current_time - s >= (5*60):
                                        if 20 <= temp_rise() <= 50:
                                                deltaT = deltaT + temp_rise()
                                                return

                                        elif 20 >= temp_rise():
                                                deltaT = deltaT + temp_rise()
                                                return 
                        
                                        elif temp_rise() > 75:
                                                deltaT = deltaT + temp_rise()
                                                deltaT = deltaT / avg
                                                blowerAmps = blowerAmps / avg
                                                inducerAmps = inducerAmps / avg
                                                c = time.ctime()
                                                log.error('furnace', '1st stage temp rise', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_temp_rise(settings[1], settings[3], settings[4]))
                                                return 

                                else:
                                        deltaT = deltaT + temp_rise()
                                        return
                        
                        else:
                                blowerAmps = (blowerAmps + blower()) / avg
                                inducerAmps = inducerAmps / avg
                                deltaT = (deltaT + temp_rise()) / avg
                                c = time.ctime()
                                log.error('furnace', '1st stage blower amps', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_blower(settings[1], settings[3], settings[4]))
                                return 
                
                else:
                        blowerAmps = (blowerAmps + blower()) / avg
                        inducerAmps = inducerAmps / avg
                        deltaT = (deltaT + temp_rise()) / avg
                        c = time.ctime()
                        log.error('furnace', '1st stage flame sensor', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_flame_sensor(settings[1], settings[3], settings[4]))
                        return 
        
        else:
                blowerAmps = (blowerAmps + blower()) / avg
                inducerAmps = (inducerAmps + inducer()) / avg
                deltaT = (deltaT + temp_rise()) / avg
                c = time.ctime()
                log.error('furnace', '1st stage inducer amps', c - s, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_inducer(settings[1], settings[3], settings[4]))
                return

# furnace stage 2 or single stage furnace
def heat_stage_two(start_time):
        global avg
        avg = avg + 1
        global settings
        global inducerAmps
        global blowerAmps
        global deltaT
        if 0.0 < inducer() < 1.8:
                inducerAmps = inducerAmp + inducer()
                if flame():
                        if 2.5 < blower() < 10:
                                blowerAmps = blowerAmps + blower()
                                current_time = time.ctime()
                                if current_time - start_time >= (5*60):
                                        if 25 <= temp_rise() <= 70:
                                                deltaT = deltaT + temp_rise()
                                                return

                                        elif 25 >= temp_rise():
                                                deltaT = deltaT + temp_rise()
                                                return
                                        elif temp_rise() > 70:
                                                deltaT = deltaT + temp_rise()
                                                deltaT = deltaT / avg
                                                blowerAmps = blowerAmps / avg
                                                inducerAmps = inducerAmps / avg
                                                log.error('furnace', 'temp rise', current_time + start_time, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_temp_rise(settings[1], settings[3], settings[4]))
                                                return
                                else:
                                        deltaT = deltaT + temp_rise()
                                        return
                        else:
                                deltaT = deltaT + temp_rise()
                                deltaT = deltaT / avg
                                blowerAmps = blowerAmps + blower()
                                blowerAmps = blowerAmps / avg
                                inducerAmps = inducerAmps / avg
                                log.error('furnace', 'Blower amps', current_time + start_time, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_blower(settings[1], settings[3], settings[4]))
                                return
                else:
                        deltaT = deltaT + temp_rise()
                        deltaT = deltaT / avg
                        blowerAmps = blowerAmps + blower()
                        blowerAmps = blowerAmps / avg
                        inducerAmps = inducerAmps / avg
                        log.error('furnace', 'Flame Sensor', current_time + start_time, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_flame_sensor(settings[1], settings[3], settings[4]))
                        return
        else:
                deltaT = deltaT + temp_rise()
                deltaT = deltaT / avg
                blowerAmps = blowerAmps + blower()
                blowerAmps = blowerAmps / avg
                inducerAmps = inducerAmps + inducer()
                inducerAmps = inducerAmps / avg
                log.error('furnace', 'Inducer amps', current_time + start_time, blowerAmps, inducerAmps, deltaT, 0.0, alerts.warning_inducer(settings[1], settings[3], settings[4]))
                return 
                

# cooling stage 1
def cool_stage_one():
        pass

# cooling stage 2 or single stage cooling
def cool_stage_two(start_time):
        global blowerAmps
        global deltaT
        global deltaE
        global settings
        s = start_time
        c = time.ctime()
        if c - s >= (5*60):
                global avg
                avg = avg + 1
                if 3.5 < blower() < 10.0:
                        blowerAmps = blowerAmps + blower()
                        if 15 < temp_drop() < 25:
                                deltaT = deltaT + temp_drop()
                                deltaE = deltaE + delta_e()
                                return
                                
                        else:
                                blowerAmps = blowerAmps / avg
                                deltaT = deltaT / avg
                                deltaE = deltaE / avg
                                c = time.ctime()
                                log.error('Cooling', 'temp drop', c - s, blowerAmps, 0.0, deltaT, deltaE, alerts.warning_temp_drop(settings[1], settings[3], settings[4]))
                                return 
                                
                else:
                        blowerAmps = blowerAmps / avg
                        deltaT = deltaT + temp_drop()
                        deltaT = deltaT / avg
                        deltaE = deltaE + delta_e()
                        deltaE = deltaE / avg
                        c = time.ctime()
                        log.error('Cooling', 'blower amps', c - s, blowerAmps, 0.0, deltaT, deltaE, alerts.warning_blower(settings[1], settings[3], settings[4]))
                        return
                        
        else:
                return
                

# hp stage 1
def hp_stage_one(start_time):
        current_time = time.ctime()
        if current_time - start_time >= (5*60):
                if 10 < temp_rise():
                        return
                else:
                        pass

        else:
                return

# hp stage 2 or single stage heatpump
def hp_stage_two(start_time):
        current_time = time.ctime()
        if current_time - start_time >= (5*60):
                if 10 < temp_rise():
                        return
                else:
                        pass

        else:
                return

# air handler
def air_handler(start_time):
        if 2.5 < blower() < 10:
                return
        else:
                pass

# air handler with heat strips
def air_handler_heat_strips(start_time):
        if 2.5 < blower() < 10:
                if 10 < temp_rise():
                        return

                else:
                        pass

        else:
                pass

def inducer():
        x = comm('f')
        print(x)
        return float(x)

def flame():
        x = comm('e')
        print(x)
        if x == '1' or 'True':
                return True

        else:
                return False

def blower():
        x = comm('g')
        print(x)
        return float(x)

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

def capacity(delta_e, cfm):
        cap = delta_e * 4.5 * cfm
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
        x = comm('a')
        print(x)
        return float(x)

def returnHumid():
        x = comm('b')
        print(x)
        return float(x)

def supplyTemp():
        x = comm('c')
        print(x)
        return float(x)

def supplyHumid():
        x = comm('d')
        print(x)
        return float(x)

def comm(z):
    # handles the communication
        import serial
        myPort = serial.Serial('/dev/ttyS1', 9600, timeout = 10)
        myPort.write(z)
        x = myPort.readline()
        myPort.close()
        return x

def w1(state):
        if state == 'on' and w_out.state == 'HIGH' or state == 'off' and w_out.state == 'LOW':
                w_out.toggle()
                
                
def w2(state):
        if state == 'on' and w2_out.state == 'HIGH' or state == 'off' and w2_out.state == 'LOW':
                w2_out.toggle()
        
                
def y1(state):
        if state == 'on' and y_out.state == 'HIGH' or state == 'off' and y_out.state == 'LOW':
                y_out.toggle()
                
                
def y2(state):
        if state == 'on' and y2_out.state == 'HIGH' or state == 'off' and y2_out.state == 'LOW':
                y2_out.toggle()
                
def g(state):
        if state == 'on' and g_out.state == 'HIGH' or state == 'off' and g_out.state == 'LOW':
                g_out.toggle()
                
def o(state):
        if state == 'on' and o_out.state == 'HIGH' or state == 'off' and o_out.state == 'LOW':
                o_out.toggle()

def cooling_call():
        start = time.ctime()
        global settings
        global blowerAmps
        global deltaT
        global deltaE
        global avg
        y_out.lo()
        g_out.lo()
        while y_read():
                c = time.ctime()
                if c - start >= 5 * 60:
                        cool_stage_two(start)
                        time.sleep(1)
                else:
                        time.sleep(1)
        y_out.hi()
        g_out.hi()
        blowerAmps = blowerAmps / avg
        deltaT = deltaT / avg
        deltaE = deltaE / avg
        cap = capacity(deltaE, settings[10])
        c = time.ctime()
        log.entry('cooling', c - start, blowerAmps, 0.0, deltaT, deltaE, cap)
        return
        
        
def startUp():
        global settings
        
        s = open('settings.txt','r')
        o = s.read()
        s.close()
        
        if o == '':
                settings.append(raw_input("Homeowner's Name?"))    #0
                settings.append(raw_input("Homeowner's E-Mail?"))  #1
                settings.append(raw_input("Contractor's Name?"))   #2
                settings.append(raw_input("Contractor's E-mail?")) #3
                settings.append(raw_input("Contractor's Phone?"))  #4
                settings.append(raw_input("Gas or Electric?"))     #5
                settings.append(raw_input("Heating Stages?"))      #6
                settings.append(raw_input("timed heat staging?"))  #7
                settings.append(raw_input("A/C or Heatpump?"))     #8
                settings.append(raw_input("Cooling Stages?"))      #9
                settings.append(raw_input("Cooling cfm?"))         #10
                
                s = open('settings.txt', 'w')
                s.write(json.dumps(settings))
                s.close()
                
        else:
                s = open('settings.txt', 'r')
                settings = json.load(s)
                s.close()
        
def t_stat():
        global settings
        if w_read():
                s = time.ctime()
                heat_call(s, settings[5], settings[6], settings[7])
        elif y_read():
                cooling_call()
        elif g_read():
                g_out.lo()
        else:
                time.sleep(1)
                

def main():
        startUp()
        while 1:
                t_stat()
        

if __name__ == '__main__':
        main()

