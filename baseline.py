#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  baseline.py
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
# This will run the first run of the equipment to handle setting a baseline
# for all future comparisons
#
import json
import Tstat
import senscom
import time

baseline = {}
boards = {}
data = {}

with open('settings.json') as f:
    base = json.load(f)

# test steady state
def testBoards():
    h = senscom.hbotPing()
    c = senscom.cbotPing()
    boards.update({'heatbot': h, 'coolbot': c})
# read all sensors
def testSensors():
    if not Tstat.tstatRead():
        sp = senscom.supplyPress
        rp = senscom.returnPress
        dp = sp - rp
        if (-3.0) <= dp <= (3.0):
            pressAdj = dp
        else:
            pressAdj = dp
            # warning high press adj check sensor
        if senscom.hbotPing():
            i = senscom.inducer()
            if i > 0.1:
                # warning ind amps sensed
                pass
            f = senscom.flame()
            if f == True:
                # warning flame sensed no call
                pass
            b = senscom.blower()
            if b > 0.1:
                # warning blower amps sensed
                pass
        if senscom.cbotPing():
            odt = senscom.odt()
            if not odt:
                # warning odt sensor failure
                pass
            cf = senscom.cond_fan
            if cf > 0.1:
                # warning cond fan amps sensed
                pass
            comp = senscom.compressor
            if comp > 0.1:
                # warning compressor amps sensed
                pass
    while Tstat.tstatRead() != 'g':
        time.sleep(1)
    st = senscom.supplyTemp()
    rt = senscom.returnTemp()
    if (-3.0) <= (st - rt) <= (3.0):
        tempAdj = st-rt
    else:
        tempAdj = st-rt
        # warning high temp adj check sensors/location
    sh = senscom.supplyHumid
    rh = senscom.returnHumid
    if (-3.0) <= (sh - rh) <= (3.0):
        humAdj = sh - rh
    else:
        humAdj = sh - rh
        # warning high humid adj check sensor/location
# heat bot
def ind(x):
    # inducer
    stage = x
    i = senscom.inducer()
    if stage = 'low':
        baseline.update({'inducer low': i})
    else:
        baseline.update({'inducer high': i})
def fla():
    # flame sensor
    fl = senscom.flame()
    return fl
def blo(c, x):
    # blower
    call = c
    stage = x
    bl = senscom.blower()
    if call == 'g':
        baseline.update({'blower fan': bl})
    elif call == 'y' and stage == 'low':
        baseline.update({'blower cool low': bl})
    elif call == 'y' and stage == 'high':
        baseline.update({'blower cool high': bl})
    elif call == 'w' and stage == 'low':
        baseline.update({'blower heat low': bl})
    elif call == 'w' and stage == 'high':
        baseline.update({'blower heat high': bl})
    else:
        pass
# main bot
    # return temp
    # supply temp
    # return press
    # supply press
    # return hum
    # supply hum
# cool bot
    # fan
    # comp
    # s line pressure
    # l line pressure

# test furnace operation and varify
# check all stages and start up
# heat start
# w1
# w2

# test a/c operation and varify
# test capacity
# y1
# y2

# test fan operationand varify

# save all results to settings.json
