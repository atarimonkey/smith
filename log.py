#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  log.py
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

import json
import logging
import time
import phant
import alerts


last_error = ''

def clear_log():
    os.remove('log')
    
def entry(c, rt, ba, ia, dt, de, cap):
    _ = StructuredMessage
    p = phant.Phant('2JrDOrmOnxt3KK1dGW1b', 'Call', 'Error', 'Run Time', 'Blower Amps', 'Inducer Amps', 'Delta T', 'Delta E', 'capacity', privatekey = 'GP8ME8GEoyCvNN2x0z27')
    logging.basicConfig(filename='log', level=logging.INFO, format='%(asctime)-15s %(message)s')
    logging.info(_(c, run_time= rt, blower_amps= ba, inducer_amps= ia,
                 delta_T= dt, delta_E= de, capacity= cap ))
    p.log(c, 'None', rt, ba, ia, dt, de, cap)
    
def error(c, e, rt, ba, ia, dt, de, cap, warning):
    # this may need to be simplified
    global last_error
    t2 = time.time()
    p = phant.Phant('2JrDOrmOnxt3KK1dGW1b', 'Call', 'Error', 'RunTime', 'BlowerAmps', 'InducerAmps', 'DeltaT', 'DeltaE', 'capacity', privatekey = 'GP8ME8GEoyCvNN2x0z27')

    if last_error == '' or (t2 - last_error) >= 86400:
        #email a warning
        warning 
        last_error = t2
        
    logging.basicConfig(filename='log.error', level=logging.ERROR, format='%(asctime)-15s %(message)s')
    logging.error(_(c, error= e, run_time= rt, blower_amps= ba, inducer_amps= ia,
                 delta_T= dt, delta_E= de ))
    p.log(c, e, rt, ba, ia, dt, de, cap)
    
class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s >>> %s' % (self.message, json.dumps(self.kwargs))



def main():
	print 'test'
	return 0

if __name__ == '__main__':
	main()

