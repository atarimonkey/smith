#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  checks.py
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


class Check():
	board = pingo.pcduino.PCDuino()

	led_pin = board.pin[13]
	led_pin.set_mode(pingo.OUTPUT)
	led_pin.lo()
	# this sets the fan out pin
	g_out = board.pin[8]
	g_out.set_mode(pingo.OUTPUT)
	g_out.lo()
	# this sets the cooling out pin
	y_out = board.pin[9]
	y_out.set_mode(pingo.OUTPUT)
	y_out.lo()
	# this sets the heat out pin
	w_out = board.pin[10]
	w_out.set_mode(pingo.OUTPUT)
	w_out.lo()
	# this sets the fan pin
	g_in = board.pin[3]
	g_in.set_mode(pingo.INPUT)
	# this sets the cooling pin
	y_in = board.pin[4]
	y_in.set_mode(pingo.INPUT)
	#this sets the heat pin
	w_in = board.pin[5]
	w_in.set_mode(pingo.INPUT)
	# this sets the second stage heat pin 
	w_two_in = board.pins[6]
	w_two_in.set_mode(pingo.INPUT)
    
    def __init__(self, heat_stages, timed,  cool_stages, hp, furnace_type, comm_speed):
        self.h_stages = heat_stages
        self.c_stages = cool_stages
        self.hp = hp
        self.f_type = furnace_type
        self.comm_speed = comm_speed
        self.timed = timed
	
	def w_read():
		# this will read the the heat terminal
		if w_in.state() == 'low' or 'LOW' or '0' or 'lo':
			return True
	
		else:
			return False
		
	def w_two_read():
		# this will read the second stage heat terminal
		if w_two_in.state() == 'low' or 'LOW' or '0' or 'lo':
			return True
		
		else:
			return False
		
	def y_read():
		# this will read the cooling terminal
		if y_in.state() == 'low' or 'LOW' or '0' or 'lo':
			return True
		
		else:
			return False
		
	def g_read():
		# this will read the fan termanal
		if g_in.state() == 'low' or 'LOW' or '0' or 'lo':
			return True
		
		else:
			return False

    # setup the equipment
    # take the info given and create a list of equipment
    def heat_call(self, start_time):
        start = start_time
        if self.f_type == "furnace":
            if self.h_stages == '2' and self.timed:
                self.heat_start()
                current_time = time.ctime()
                while (current_time - start) < (9*60) and self.w_read():
                    self.heat_stage_one(start)
                    current_time = time.ctime()
                while self.w_read():
                    self.heat_stage_two(start)
                return

            elif self.h_stages == '2' and self.timed == False:
                self.heat_start()
                time.sleep(30)
                while self.w_read() and not self.w_two_read():
                    self.heat_stage_one(start)
                while self.w_two_read():
                    self.heat_stage_two(start)
                return

            else:
                self.heat_start()
                time.sleep(30)
                while self.w_read():
                    self.heat_stage_two(start)
                return

        elif self.f_type == "air handler with heat strips":
            while self.w_read():
                self.air_handler_heat_strips(start)
            return

    # start the furnace
    def heat_start(self):
        if self.inducer() > 0:
            time.sleep(30)
            f = 0
            p = 0
            while p < 3:
                if p == 0 and self.flame():
                    f = 1
                    p += 1
                    time.sleep(2)
                    return

                elif p == 0 and not self.flame():
                    p += 1
                    time.sleep(2)
                    return

                elif p > 0 and f == 0:
                    if not self.flame():
                        p += 1
                        time.sleep(2)
                        return

                    else:
                        f = 1
                        p += 1
                        time.sleep(2)
                        return

                elif p > 0 and f == 1:
                    p += 1
                    time.sleep(2)
                    return

            if self.flame():
                b = 0
                while self.blower() == 0:
                    if b >= 123:
                        pass

                    else:
                        time.sleep(1)
                        b +=1
                        return
                if 2.5 < self.blower() > 10:
                    return True

                else:
                    pass

            elif f == 0 and not self.flame():
                pass

            elif f == 1 and not self.flame():
                pass

        else:
            pass

    # furnace stage 1
    def heat_stage_one(self, start_time):
        if 0.0 < self.inducer() < 1.0:
            if self.flame():
                if 2.5 < self.blower() < 10:
                    current_time = time.ctime()
                    if current_time - start_time >= (5*60):
                        if 20 < self.temp_rise() <= 50:
                            return

                        elif 20 >= self.temp_rise():
                            

                        elif self.temp_rise() > 50:
                            pass

                    else:
                        return

                else:
                    pass

            else:
                pass

        else:
            pass

    # furnace stage 2 or single stage furnace
    def heat_stage_two(self, start_time):
        if 0.0 < self.inducer() < 1.8:
            if self.flame():
                if 2.5 < self.blower() < 10:
                    current_time = time.ctime()
                    if current_time - start_time >= (5*60):
                        if 25 < self.temp_rise() <= 70:
                            return

                        elif 25 >= self.temp_rise():
                            pass

                        elif self.temp_rise() > 70:
                            pass

                    else:
                        return

                else:
                    pass

            else:
                pass

        else:
            pass

    # cooling stage 1
    def cool_stage_one(self):
        pass

    # cooling stage 2 or single stage cooling
    def cool_stage_two(self):
        pass

    # hp stage 1
    def hp_stage_one(self, start_time):
        current_time = time.ctime()
        if current_time - start_time >= (5*60):
            if 10 < self.temp_rise():
                return
            else:
                pass

        else:
            return

    # hp stage 2 or single stage heatpump
    def hp_stage_two(self, start_time):
        current_time = time.ctime()
        if current_time - start_time >= (5*60):
            if 10 < self.temp_rise():
                return
            else:
                pass

        else:
            return

    # air handler
    def air_handler(self, start_time):
        if 2.5 < self.blower() < 10:
            return
        else:
            pass

    # air handler with heat strips
    def air_handler_heat_strips(self, start_time):
        if 2.5 < self.blower() < 10:
            if 10 < self.temp_rise():
                return

            else:
                pass

        else:
            pass

    def inducer(self):
        x = float(self.comm('f'))
        return x

    def flame(self):
        x = self.comm('e')
        if x == '1' or 'True':
            return True
        else:
            return False

    def blower(self):
        x = float(self.comm('g'))
        return x

    def temp_rise(self):
        deltaT = self.supplyTemp() - self.returnTemp()
        return deltaT

    def temp_drop(self):
        deltaT = self.returnTemp() - self.supplyTemp()
        return deltaT

    def delta_h(self):
        d = self.returnHumid() - self.supplyHumid()
        return d

    def delta_e(self):
        e = self.entholpy(self.returnTemp(), self.returnHumid()) - self.entholpy(self.supplyTemp(), self.supplyHumid())
        return e

    def capacity(self, cfm):
        cap = self.delta_e() * 4.5 * cfm
        return cap

    def entholpy(self, temp, humid):
        t = temp + 459.67
        n = math.log(t)
        l = -10440.4 / t - 11.29465 - 0.02702235 * t + 0.00001289036 * t ** 2 - 0.000000002478068 * t ** 3 + 6.545967 * n
        s = math.exp(l)
        p = humid / 100 * s
        w = 0.62198 * p / (14.7 - p)
        h = 0.24 * temp + w * (1061 + 0.444 * temp)
        return h

    def returnTemp(self):
        x = float(self.comm('a'))
        return x

    def returnHumid(self):
        x = float(self.comm('b'))
        return x

    def supplyTemp(self):
        x = float(self.comm('c'))
        return x

    def supplyHumid(self):
        x = float(self.comm('d'))
        return x

    def comm(self, z):
        # handles the communication
        import serial
        myPort = serial.Serial('/dev/ttyS1', self.comm_speed, timeout = 10)
        myPort.write(z)
        x = myPort.readline()
        myPort.close()
        return x


def main():
	
	return 0

if __name__ == '__main__':
	main()

