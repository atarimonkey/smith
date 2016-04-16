#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  skynet.py
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
# version 0.1

import Json, pingo, time, checks


settings = []
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

def heat():
	# starts the heating call
	w_out.hi() # provides 24v out
	
	
def startUp:
	global settings
	
	s = open('settings.txt','r')
	o = s.read()
	s.close()
	
	if o == '':
		settings.append(input("Homeowner's Name?"))
		settings.append(input("Homeowner's E-Mail?"))
		settings.append(input("Contractor's Name?"))
		settings.append(input("Contractor's E-mail?"))
		settings.append(input("Contractor's Phone?"))
		settings.append(input("Gas or Electric?"))
		settings.append(input("Heating Stages?"))
		settings.append(input("A/C or Heatpump?"))
		settings.append(input("Cooling Stages?"))
		settings.append(input("ECM or PSC?"))
		
		s = open('settings.txt', 'w')
		s.write(json.dumps(settings))
		s.close()
		
	else:
		s = open('settings.txt', 'r')
		settings = json.load(s)
		s.close()
		
def t_stat():
	if w_read():
		

def main():
	
	return 0

if __name__ == '__main__':
	main()

