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
import time
import compare
import Tstat

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

    def general_heat(self, t, stage):
        s = stage
        if self.timed_stages:
            if t < 600:
                s = 'low'
            else:
                s = 'high'

        if compare.staticPressureCheck():
            if t >= 420:
                if compare.tempRiseGas(s) == 'norm':
                    return True
                elif compare.tempRiseGas(s) == 'high':
                    # troubleshoot mode
                    if self.troubleshoot_gen_furn(t):
                        return False
                    else:
                        return True
                elif compare.tempRiseGas(s) == 'low':
                    # troubleshoot mode
                    if self.troubleshoot_gen_furn(t):
                        return False
                    else:
                        return True
            else:
                return True
        else:
            # troubleshoot mode
            if self.troubleshoot_gen_furn(t):
                return False
            else:
                return True

    def troubleshoot_gen_furn(t):
        static = ''
        delta_T = ''
        s = ''

        if self.timed_stages:
            if Tstat.heat_read() == 'w1' or Tstat.heat_read() == 'w2':
                if t < 600:
                    s = 'low'
                else:
                    s = 'high'
            else:
                return True
        else:
            if Tstat.heat_read() == 'w1':
                s = 'low'
            elif Tstat.heat_read() == 'w2':
                s = 'high'
            else:
                return False

        static = compare.staticPressureCheck()
        delta_T = compare.tempRiseGas()

        if static:
            if t > 420:
                if delta_T == 'norm':
                    return False
                elif delta_T == 'low':
                    #error 2 - low temp rise
                    return True
                elif delta_T == 'high':
                    #error 1 - filter / airflow
                    return True
            else:
                return False
        else:
            # error 1 - filter / airflow

    def troubleshoot_furnace(self, f, t):
        burners = f
        ind = ''
        fla = ''
        blo = ''
        delta_T = ''
        stage = ''

        if self.timed_stages:
            if Tstst.heat_read() == 'w2' or Tstat.heat_read() == 'w1':
                if t < 600:
                    stage = 'low'
                else:
                    stage = 'high'
        else:
            if Tstat.heat_read() == 'w1':
                stage = 'low'
            elif Tstat.heat_read() == 'w2':
                stage = 'high'
            else:
                return False

        if stage == True:
            ind = compare.altInducerAmps(stage)
            fla = compare.flameCheck()
            blo = compare.altBlowerAmps('w', stage)
            delta_T = compare.tempRiseGas(stage)
            static = compare.staticPressureCheck()
            if ind == True:
                if fla == True:
                    # needs a way to tell if it lit or not
                    if blo == True:
                        if delta_T == 'norm':
                            if static:
                                return False
                        elif delta_T == 'low':
                            # setting error
                            return True
                        elif delta_T == 'high':
                            # error 1 - filter / airflow
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

    def troubleshoot_condenser(self):
        cond_fan = ''
        compressor = ''
        odt = ''
        stage = ''

        if Tstat.cool_read() == 'y':
            stage = 'low'
        elif Tstat.cool_read() == 'y2':
            stage = 'high'
        else:
            return False

        if stage == True:
            odt = senscom.odt()
            cond_fan = compare.cond_fan_check(stage)
            compressor = compare.comp_check(stage)
            if odt > 65.0:
                if cond_fan == True:
                    if compressor == True:
                        return False
                    else:
                        #compressor issue
                        return True
                else:
                    #fan issue
                    return True
            else:
                #too cold to test properly
                return True

    def troubleshoot_cooling_indoor(self):
        stage = ''
        blower = ''
        deltaT = ''
        capacity = ''
        static = ''

        if Tstat.cool_read() == 'y':
            stage = 'low'
        elif Tstat.cool_read() == 'y2':
            stage = 'high'
        else:
            return False

        blower = compare.altBlowerAmps('y', stage)
        deltaT = compare.tempDrop(stage)
        capacity = compare.capacityCheck(self.cooling_tonage, self.cooling_cfm)
        static = compare.stacicPressureCheck()

        if blower == True:
            if deltaT == True:
                if capacity == True:
                    return False
                else:
                    if static == True
                        if self.coolBot == True:
                            if self.troubleshoot_condenser() == True:
                                # low refrigerant
                                return True
                            else:
                                pass
                        else:
                            #low refrigerant / condenser issue
                    else:
                        #airflow
                        return True
            else:
                if static == True:
                    if self.coolBot == True:
                        if self.troubleshoot_condenser() == True:
                            # airflow issues / clogged filter
                            return True
                        else:
                            pass
                    else:
                        # condenser issue
                        return True
                else:
                    #airflow issue
                    return True
        else:
            # blower issue
            return True

    def troubleshoot_hp_indoor(self):
        stage = ''
        blower = ''
        deltaT = ''
        static = ''

        if Tstat.cool_read() == 'y' and Tstat.reversing() and not Tstat.heat_read():
            stage = 'low'
        elif Tstat.cool_read() == 'y2' and Tstat.reversing() and not Tstat.heat_read():
            stage = 'high'
        elif Tstat.cool_read() and Tstat.reversing() and Tstat.heat_read():
            stage = 'aux'
        else:
            return False

        blower = compare.altBlowerAmps('y', stage)
        deltaT = compare.tempRiseHp(stage)
        static = compare.stacicPressureCheck()

        if blower == True:
            if deltaT == True:
                return False
            else:
                if static == True
                    if self.coolBot == True:
                        if self.troubleshoot_condenser() == True:
                            # low refrigerant/ defrost/ condenser issue
                            return True
                        else:
                            pass
                    else:
                        #low refrigerant / condenser issue
                else:
                    #airflow
                    return True
        else:
            if static == True:
                if self.coolBot == True:
                    if self.troubleshoot_condenser() == True:
                        # airflow issues / clogged filter
                        return True
                    else:
                        pass
                else:
                    # condenser issue
                    return True
            else:
                #airflow issue
                return True
        else:
            # blower issue
            return True

    def troubleshoot_geo(self):
        stage = ''
        blower = ''
        deltaT = ''
        capacity = ''
        static = ''
        comp = ''
        pumps = ''

        if Tstat.cool_read() == 'y'and not Tstat.reversing and not Tstat.heat_read():
            stage = 'low'
        elif Tstat.cool_read() == 'y2' and not Tstat.reversing and not Tstat.heat_read():
            stage = 'high'
        if Tstat.cool_read() == 'y'and Tstat.reversing and not Tstat.heat_read():
            stage = 'low'
        elif Tstat.cool_read() == 'y2' and Tstat.reversing and not Tstat.heat_read():
            stage = 'high'
        elif Tstat.cool_read() and Tstat.reversing and Tstat.heat_read():
            stage = 'aux'
        else:
            return False

        if Tstat.reversing():
            deltaT = compare.tempRiseHp(stage)
        else:
            deltaT = compare.tempDrop(stage)

        blower = compare.altBlowerAmps(stage)
        capacity = compare.capacityCheck(self.cooling_tonage, self.cooling_cfm)
        static = compare.staticPressureCheck()
        comp = compare.comp_check(stage)
        pumps = compare.pump_check()

        if stage:
            if pumps:
                if comp:
                    if blower:
                        if static:
                            if deltaT:
                                if not Tstat.reversing():
                                    if capacity:
                                        return False
                                    else:
                                        # low water/ refrigerant
                                        return True
                                else:
                                    return False
                            else:
                                # low water/ refrigerant
                                return True
                        # clogged filter/ airflow restiction
                        return True
                    else:
                        # bad blower
                        return True
                else:
                    # bad compressor
                    return True
            else:
                # bad pumps
                return True

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

    def furnace_timed(self, t):
        if t < 600:
            stage = 'low'
        else:
            stage = 'high'

        if compare.altInducerAmps(stage) == True:
            if compare.flameCheck() == True:
                if compare.altBlowerAmps('w', stage) == True:
                    if compare.tempRiseGas(stage) == True:
                        return True
                    else:
                        # troubleshoot mode
                        Equipment.troubleshoot_furnace(True, t)
                        return False
                else:
                    #troubleshoot mode
                    Equipment.troubleshoot_furnace(True, t)
                    return False
            else:
                #troubleshoot mode
                Equipment.troubleshoot_furnace(True, t)
                return False
        else:
            #troubleshoot mode
            Equipment.troubleshoot_furnace(True, t)
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
                    if compare.altBlowerAmps('y', stage):
                        if p > 4:
                            if compare.tempDrop(stage) == True:
                                if compare.capacityCheck(self.cooling_tonage, self.cooling_cfm) == True:
                                    return True
                                else:
                                    if Equipment.troubleshoot_cooling_indoor() == True:
                                        return False
                                    else:
                                        return True
                            else:
                                if Equipment.troubleshoot_cooling_indoor() == True:
                                    return False
                                else:
                                    return True
                        else:
                            return True
                    else:
                        if Equipment.troubleshoot_cooling_indoor() == True:
                            return False
                        else:
                            return True
                else:
                    if Equipment.troubleshoot_cooling_indoor() == True:
                        return False
                    else:
                        return True
            else:
                if Equipment.troubleshoot_cooling_indoor() == True:
                    return False
                else:
                    return True
        else:
            if compare.altBlowerAmps('y', stage) == True:
                if p > 4:
                    if compare.tempDrop(stage) == True:
                        if compare.capacityCheck(self.cooling_tonage, self.cooling_cfm) == True:
                            return True
                        else:
                            if Equipment.troubleshoot_cooling_indoor() == True:
                                return False
                            else:
                                return True
                    else:
                        if Equipment.troubleshoot_cooling_indoor() == True:
                            return False
                        else:
                            return True
                else:
                    return True
            else:
                if Equipment.troubleshoot_cooling_indoor() == True:
                    return False
                else:
                    return True

    def hp(self, p, stage):
        t = 0
        if self.coolBot == True:
            time.sleep(1)
            t = t + 1
            if compare.condenserFan(stage) == True:
                time.sleep(1)
                t = t + 1
                if compare.compresser(stage) == True:
                    if compare.altBlowerAmps('y', stage):
                        if p > 4:
                            if compare.tempRiseHp(stage) == True:
                                return True
                            else:
                                if Equipment.troubleshoot_hp_indoor() == True:
                                    return False
                                else:
                                    return True
                        else:
                            return True
                    else:
                        if Equipment.troubleshoot_hp_indoor() == True:
                            return False
                        else:
                            return True
                else:
                    if Equipment.troubleshoot_hp_indoor() == True:
                        return False
                    else:
                        return True
            else:
                if Equipment.troubleshoot_hp_indoor() == True:
                    return False
                else:
                    return True
        else:
            if compare.altBlowerAmps('y', stage) == True:
                if p > 4:
                    if compare.tempRiseHp(stage) == True:
                        return True
                    else:
                        if Equipment.troubleshoot_hp_indoor() == True:
                            return False
                        else:
                            return True
                else:
                    return True
            else:
                if Equipment.troubleshoot_hp_indoor() == True:
                    return False
                else:
                    return True

    def geo_cool(self, p, stage):
        t = 0
        while t == 0:
            time.sleep(1)
            t = t + 1
        if compare.compressor(stage):
            if compare.altBlowerAmps('y', stage):
                if p > 4:
                    if compare.tempDrop(stage):
                        if compare.capacityCheck(self.cooling_tonage, self.cooling_cfm):
                            return True
                        else:
                            if equipment.troubleshoot_geo():
                                return False
                            else:
                                return True
                    else:
                        if equipment.troubleshoot_geo():
                            return False
                        else:
                            return True
                else:
                    return True
            else:
                if equipment.troubleshoot_geo():
                    return False
                else:
                    return True
        else:
            if equipment.troubleshoot_geo():
                return False
            else:
                return True





def main():

    return 0

if __name__ == '__main__':
    main()

