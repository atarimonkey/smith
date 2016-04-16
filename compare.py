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
		

# check the flame sensor

# check the temp rise

# check the temp drop

# check capacity



def main():
	
	return 0

if __name__ == '__main__':
	main()

