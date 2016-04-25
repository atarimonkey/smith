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
		
	def troubleshoot_furnace(self, f):
		burners = f
		ind = ''
		fla = ''
		blo = ''
		delta_T = ''
		stage = ''
		
		if Tstat.heat_read() == 'w1':
			stage = 'low'
		elif Tstat.heat_read() == 'w2':
			stage = 'high'
		else:
			pass
		
		if stage == True:
			ind = compare.altInducerAmps(stage)
			fla = compare.flameCheck()
			blo = compare.altBlowerAmps('w', stage)
			delta_T = compare.tempRiseGas(stage)
			if ind == True:
				if fla == True:
					# needs a way to tell if it lit or not
					if blo == True:
						if delta_T == True:
							return False
						else:
							# airflow error
							return True
					else:
						# blower error
						return True
				elif burners == True and not fla:
					# flame senser error
					return True
				elif burners and fla == False:
					# ignitor/ gas valve error
					return True
				else:
					# ignitor/gas/flame sensor error
					return True
			else:
				# inducer error
				return True
		else:
			return False

class GasFurnace(Equipment):
	def __init__(self, heat_stages, timed_stages, heatBot):
		super(GasFurnace, self).__init__(self, 'furnace', heat_stages, timed_stages, heatBot)
		self.heat_stages = heat_stages
		self.timed_stages = timed_stages
		self.heatBot = heatBot
			
	def furnace_stage(self, stage):
		if compare.altInducerAmps(stage) == True:
			if compare.flameCheck() == True:
				if compare.altBlowerAmps('w', stage) == True:
					if compare.tempRiseGas(stage) == True:
						return True
					else:
						# troubleshoot mode
						Equipment.troubleshoot_furnace(True)
						return False
				else:
					#troubleshoot mode
					Equipment.troubleshoot_furnace(True)
					return False
			else:
				#troubleshoot mode
				Equipment.troubleshoot_furnace(True)
				return False
		else:
			#troubleshoot mode
			Equipment.troubleshoot_furnace(True)
			return False
		
	def furnace_start(self, stage):
		t = 0
		if compare.altInducerAmps('high'):
			while t < 30:
				t = t + 1
				time.sleep(1)
			if compare.flameCheck():
				while t < 33:
					t = t + 1
					time.sleep(1)
				if compare.flameCheck():
					while t < 95:
						t = t + 1
						time.sleep(1)
					if compare.altBlowerAmps('w', stage):
						return True
					else:
						# troubleshoot mode
						Equipment.troubleshoot_furnace(True)
						return False
				else:
					# troubleshoot
					Equipment.troubleshoot_furnace(True)
					return False
			else:
				# troubleshoot
				Equipment.troubleshoot_furnace(False)
				return False
		else:
			#troubleshoot
			Equipment.troubleshoot_furnace(False)
			return False
	
class Condenser(Equipment):

    def __init__(self, heatpump, cooling_stages, cooling_tonage, cooling_cfm, coolBot):
        super(Condenser, self).__init__('none', 'none', 'none', 'none', heatpump, cooling_stages, cooling_tonage, cooling_cfm, coolBot)
        self.heatpump = heatpump
        self.cooling_stages = cooling_stages
        self.cooling_tonage = cooling_tonage
        self.cooling_cfm = cooling_cfm
        self.coolBot = coolBot

    def cooling(self, p, stage):
        t = 0
        if self.coolBot == True:
            time.sleep(1)
            t = t + 1
            if compare.condenserFan(stage) == True:
                time.sleep(1)
                t = t + 1
                if compare.compresser(stage) == True:
                    if p > 4:
                        if compare.tempdrop(stage) == True:



def main():
	
	return 0

if __name__ == '__main__':
	main()

