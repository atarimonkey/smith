#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  start.py
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
import json
import garvis
import Tstat
import time

with open('settings.json') as data_file:
    data = json.load(data_file)

if data["contact"]['name'] == '':
    # download setting.json
    pass

hType = data["equipment"]['heat type']
hStages = data["equipment"]['heat stages']
timed = data["equipment"]['timed stages']
hBot = data["board"]['heatbot']
hp = data["equipment"]['heatpump']
cStages = data["equipment"]['cooling stages']
cTon = data["equipment"]['cooling tonage']
cfm = data["equipment"]['cooling cfm']
cBot = data["board"]['coolbot']

def start():
    heat = garvis.GasFurnace(hStage, timed, hBot)
    cool = garvis.Condenser(hp, cStages, cTon, cfm, cBot)

def main():
    stat = Tstat.tstatRead()
    if stat = 'w1':
        heat.furnaceCall()
    elif stat = 'w2':
        heat++.furnaceCall()
    elif stat = 'y1':
        pass
    elif stat = 'y2':
        pass
    elif stat = 'g':
        pass
    time.sleep(1)

if __name__ == __main__:
    start()
    while 1:
        main()