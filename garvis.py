#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  garvis.py
#  
#  Copyright 2016 David Keuchel <david.keuchel@gmail.com>
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
import time, compare

class Equipment(object):	
	def __init__(heat_type, heat_stages, timed_stages, heatBot, heatpump, cooling_stages, cooling_tonage, cooling_cfm, coolBot):
		self.heat_type = heat_type
		self.heat_stages = heat_stages
		self.timed_stages = timed_stages
		self.heatpump = heatpump
		self.heatBot = heatBot
		self.cooling_stages = cooling_stages
		self.cooling_tonage = cooling_tonage
		self.cooling_cfm = cooling_cfm
		self.coolBot
		
class GasFurnace(Equipment):
	def __init__(self, heat_stages, timed_stages, heatBot):
		Equipment.__init__(self, 'furnace', heat_stages, timed_stages, heatBot
		self.heat_stages = heat_stages
		self.timed_stages = timed_stages
		self.heatBot = heatBot
			
	def furnace_stage(self, stage):
		if compare.altInducerAmps(stage) == True:
			if compare.flameCheck() == True:
				if compare.altBlowerAmps(stage) == True:
					if compare.tempRiseGas(stage) == True:
						return True
					else:
						# troubleshoot mode
						return False
				else:
					#troubleshoot mode
					return False
			else:
				#troubleshoot mode
				return False
		else:
			#troubleshoot mode
			return False
		
	def furnace_start(self):
		t = 0
		if compare.altInducerAmps('high'):
			


def main():
	
	return 0

if __name__ == '__main__':
	main()

