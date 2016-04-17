#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  compare.py
#  
#  Copyright 2016 David Keuchel <david@david-Inspiron-3521>
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

import senscom, time,

blowerLow = ''
blowerMed = ''
blowerHi = ''

inducerLow = ''
inducerHi = ''

# check the blower amps
def blowerAmps(speed):
	if speed == 'low':
		if 0.5 <= senscom.blower() <= 2.6:
			# log data
			return True
		else:
			return False
	elif speed == 'med':
		if 1.0 <= senscom.blower() <= 4.6:
			# log data
			return True
		else:
			return False
	elif speed == 'high':
		if 4.5 <= senscom.blower() <= 10.0:
			# log data
			return True
		else:
			return False
	else:
		if 2.0 <= senscom.blower() <= 10.0:
			# log data
			return True
		else:
			return False

# alt blower check
def altBlowerAmps(speed):
	if speed == 'low':
		if blowerLow == '':
			blowerLow = senscom.blower()
			s = blowerLow
		else:
			s = blowerLow
	elif speed == 'med':
		if blowerMed == '':
			blowerMed = senscom.blower()
			s = blowerMed
		else:
			s = blowerMed
	elif speed == 'high':
		if blowerHi == '':
			blowerHi = senscom.blower()
			s = blowerHi
		else:
			s = blowerHi
		
	if (s * .9) <= senscom.blower() <= (s * 1.1):
		# log data
		return True
	else:
		return False
		

# check the inducer amps
def inducerAmps(stage):
	if stage == 'low':
		if 0.5 < senscom.inducer() < 1.3:
			# log data
			return True
		else:
			return False
	else:
		if 0.5 < senscom.inducer() 2.0:
			# log data
			return True
		else:
			return False

def altInducerAmps(speed):
	if speed == 'low':
		if inducerLow == '':
			inducerLow = senscom.inducer()
			s = inducerLow
	else:
		if inducerHi == '':	
			inducerHi = senscom.inducer()
			s = inducerHi
	
	if (s * .9) <= senscom.inducer() <= (s * 1.1):
		# log data
		return True
	else:
		return False

# check the flame sensor
def flameCheck():
	if senscom.flame() == 'True':
		# log data
		return True
	else:
		return False
		
# check the temp rise
def tempRiseGas(stage):
	if stage == 'low':
		if 20 <= senscom.temp_rise() <= 35:
			#log data
			return True
		else:
			return False
	else:
		if 30 <= senscom.temp_rise() <= 70:
			#log data
			return True
		else:
			return False
		
# check the temp drop
def tempDrop(stage):
	if stage == 'low':
		if 15 <= senscom.temp_drop() <= 20:
			#log data
			return True
		else:
			return False
	else:
		if 18 <= senscom.temp_drop() <= 26:
			#log data
			return True
		else:
			return False

# check capacity
def capacityCheck(tonage, cfm):
	btu = ''
	if tonage == 1.5:
		btu = 18000
	elif tonage == 2:
		btu = 24000
	elif tonage == 2.5:
		btu = 30000
	elif tonage == 3:
		btu = 36000
	elif tonage == 3.5:
		btu = 42000
	elif tonage == 4:
		btu = 48000
	elif tonage == 5:
		btu = 60000
	else:
		pass
	
	if (btu * .9) <= senscom.capacity(cfm) <= (btu * 1.1):
		#log data
		return True
	else:
		return False

def main():
	
	return 0

if __name__ == '__main__':
	main()

