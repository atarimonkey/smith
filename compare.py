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

import senscom
import Json

with open('settings.json') as data_file:
    data = json.load(data_file)

blowerHeatLow = data["baseline"]['blower heat low']
blowerHeatHi = data["baseline"]['blower heat high']
blowerCoolLow = data["baseline"]['blower cool low']
blowerCoolHi = data["baseline"]['blower cool high']
blowerFan = data["baseline"]['blower fan']

inducerLow = data["baseline"]["inducer low"]
inducerHi = data["baseline"]['inducer high']

condFanLow = data["baseline"]['cond fan low']
condFanHi = data["baseline"]['cond fan high']

compLow = data["baseline"]['comp low']
compHi = data["baseline"]['comp high']

pressure = data["baseline"]['pressure']

pumpAmps = data["baseline"]['pump']

# check the blower amps
def blowerAmps(speed):
    #log data
    if speed == 'low':
        if 0.5 <= senscom.blower() <= 2.6:
            return True
        else:
            return False
    elif speed == 'med':
        if 1.0 <= senscom.blower() <= 4.6:
            return True
        else:
            return False
    elif speed == 'high':
        if 4.5 <= senscom.blower() <= 10.0:
            return True
        else:
            return False
    else:
        if 2.0 <= senscom.blower() <= 10.0:
            return True
        else:
            return False

# alt blower check
def altBlowerAmps(call, speed):
    global blowerHeatLow
    global blowerHeatHi
    global blowerCoolLow
    global blowerCoolHi
    global blowerFan
    if call == 'w':
        if speed == 'low':
            if blowerHeatLow == '':
                blowerHeatLow = senscom.blower()
                s = blowerHeatLow
            else:
                s = blowerHeatLow
        elif speed == 'high':
            if blowerHeatHi == '':
                blowerHeatHi = senscom.blower()
                s = blowerHeatHi
            else:
                s = blowerHeatHi
    elif call == 'y':
        if speed == 'low':
            if blowerCoolLow == '':
                blowerCoolLow = senscom.blower()
                s = blowerCoolLow
            else:
                s = blowerCoolLow
        else:
            if blowerCoolHi == '':
                blowerCoolHi = senscom.blower()
                s = blowerCoolHi
            else:
                s = blowerCoolHi
    elif call == 'g':
        if blowerFan == '':
            blowerFan = senscom.blower()
            s = blowerFan
        else:
            s = blowerFan

    #log data

    if (s * .9) <= senscom.blower() <= (s * 1.1):
        return 'norm'
    elif (s * .1) < senscom.blower() < (s * .9):
        return 'low'
    elif senscom.blower() > (s * 1.1):
        return 'high'
    else:
        return False

# check the inducer amps
def inducerAmps(stage):
    #log data
    if stage == 'low':
        if 0.5 < senscom.inducer() < 1.3:
            return True
        else:
            return False
    else:
        if 0.5 < senscom.inducer() 2.0:
            return True
        else:
            return False

def altInducerAmps(speed):
    global inducerLow
    global inducerHi
    if speed == 'low':
        if inducerLow == '':
            inducerLow = senscom.inducer()
            s = inducerLow
    else:
        if inducerHi == '':	
            inducerHi = senscom.inducer()
            s = inducerHi

    # log data

    if (s * .9) <= senscom.inducer() <= (s * 1.1):
        return 'norm'
    elif (s * .1) < senscom.inducer() < (s * .9):
        return 'low'
    elif senscom.inducer() > (s * 1.1):
        return 'high'
    else:
        return False

# check the flame sensor
def flameCheck():
    # log data
    if senscom.flame() == 'True':
        return True
    else:
        return False

# check the temp rise
def tempRiseGas(stage):
    # log data
    if stage == 'low':
        if 20 <= senscom.temp_rise() <= 35:
            return 'norm'
        elif senscom.temp_rise() < 5:
            return False
        elif 5 < senscom.temp_rise() < 20:
            return 'low'
        elif senscom.temp_rise() > 35:
            return 'high'
    else:
        if 30 <= senscom.temp_rise() <= 70:
            return 'norm'
        elif senscom < 5:
            return False
        elif 5 < senscom.temp_rise() < 30:
            return 'low'

def tempRiseHp(stage):
    if stage == 'low':
        if 14 <= senscom.temp_rise() <= 20:
            return 'norm'
        elif senscom.temp_rise() <= 5:
            return False
        elif 5 < senscom.temp_rise() < 14:
            return 'low'
        elif senscom.temp_rise() > 20:
            return 'high'
    elif stage == 'high':
        if 18 <= senscom.temp_rise() <= 30:
            return 'norm'
        elif 5 < senscom.temp_rise() < 18:
            return 'low'
        elif senscom.temp_rise() > 30:
            return 'high'
        else:
            return False
    elif stage == 'aux':
        if 20 <= senscom.temp_rise() <= 40:
            return 'norm'
        elif 5 < senscom.temp_rise() < 20:
            return 'low'
        elif senscom.temp_rise() > 40:
            return 'high'
        else:
            return False


# check the temp drop
def tempDrop(stage):
    #log data
    if stage == 'low':
        if 14 <= senscom.temp_drop() <= 20:
            return 'norm'
        elif 5 < senscom.temp_drop() < 14:
            return 'low'
        elif senscom.temp_drop() > 20:
            return 'high'
        else:
            return False
    else:
        if 16 <= senscom.temp_drop() <= 26:
            return 'norm'
        elif 5 < senscom.temp_drop() < 16:
            return 'low'
        elif senscom.temp_drop() > 26:
            return 'high'
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

    #log data

    if (btu * .9) <= senscom.capacity(cfm) <= (btu * 1.1):
        return 'norm'
    elif (btu * .9) > senscom.capacity(cfm):
        return 'low'
    else:
        return False

def staticPressureCheck():
    global pressure
    p = senscom.supplyPress() + senscom.returnPress

    if pressure == '':
        pressure = p

    # log pressure

    if (pressure * .9) < p < (pressure * 1.1):
        return 'norm'
    elif p < (pressure * .9):
        return 'low'
    elif p > (pressure * 1.1):
        return 'high'
    else:
        return False

def cond_fan_check(stage):
    global condFanLow
    global condFanHi
    if stage == 'low':
        if condFanLow == '':
            condFanLow = senscom.cond_fan()
            f = condFanLow
        else:
            f = condFanLow
    else:
        if condFanHi == '':
            condFanHi = senscom.cond_fan()
            f = condFanHi
        else:
            f = condFanHi

    #log data

    if (f * .9) < senscom.cond_fan() < (f * 1.1):
        return 'norm'
    elif (f * .1) < senscom.cond_fan() < (f * .9):
        return 'low'
    elif senscom.cond_fan() > (f * 1.1):
        return 'high'
    else:
        return False

def comp_check(stage):
    global compLow
    global compHi
    if stage == 'low':
        if compLow == '':
            compLow = senscom.compressor()
            c = compLow
        else:
            c = compLow
    else:
        if compHi == '':
            compHi = senscom.compressor()
            c = compHi
        else:
            c = compHi

    #log data

    if (c * .9) <= senscom.compressor() <= (c * 1.1):
        return 'norm'
    elif (c * .1) < senscom.compressor() < (c * .9):
        return 'low'
    elif senscom.compressor() > (c * 1.1):
        return 'high'
    else:
        return False

def pump_check():
    global pumpAmps

    if pumpAmp == '':
        pumpAmps = senscom.pump()

    p = pumpAmps

    #log data

    if (p * .9) <= senscom.pump() <= (p * 1.1):
        return 'norm'
    elif (p * .1) < senscom.pump() < (p * .9):
        return 'low'
    elif senscom.pump() > (p * 1.1):
        return 'high'
    else:
        return False

def main():

    return 0

if __name__ == '__main__':
    main()

