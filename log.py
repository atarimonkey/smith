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
import logging.handlers
import time
import phant


last_error = ''


class Log:
    """This class is to facilitate the logging of the mesurements or errors in each of your modules"""
    def __init__(self, logname):
        """This is used to build the logger for the module you are calling this from.  You should create a new logger for
        each module you want to log from.  Usage:  logger = log.Log(modlule_name)"""
        assert type(logname) is str, "Invalid Log Name"
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(logging.INFO)
        self.log_file = logging.handlers.RotatingFileHandler("{0}.txt".format(logname), maxBytes=10485760,
                                                             backupCount=1)
        self.log_file.setLevel(logging.INFO)
        self.logger.addHandler(self.log_file)
        self.file_formatter = logging.Formatter('%(asctime)s  %(name)s:%(levelname)s: %(message)s',
                                                datefmt='%Y/%m/%d %H:%M:%S')
        self.log_file.setFormatter(self.file_formatter)
        self.web_logger = phant.Phant('2JrDOrmOnxt3KK1dGW1b', 'bloweramps', 'call', 'capacity', 'deltae', 'deltat',
                                      'error', 'induceramps', 'runtime', private_key='GP8ME8GEoyCvNN2x0z27')

    def log_to_file(self, message):
        """This function is used to log  a message to the log file defined for this module.
        Usage: logger.log_to_file('Data to be logged')"""
        assert type(message) is str, "Invalid log data"
        self.logger.info(message)

    def log_to_web(self, blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time):
        """This function is used to send log data to phant
        Usage:  logger.log_to_web(call, error, run_time, blower_amps, inducer_amps, delta_t, delta_e, capacity)"""
        self.web_logger.log(blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time)

    def log_to_all(self, blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time):
        """This function loggs to a file and sends log data to phant
        Usage:  logger.log_to_all(call, error, run_time, blower_amps, inducer_amps, delta_t, delta_e, capacity)"""
        self.web_logger.log(blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time)
        self.logger.info("Runtime={7}, Delta T={4}, Inducer Amps={6}, Error={5}, Delta E={3}, Call={1}, " \
                         "Blower Amps={0}, Capacity={2}".format(blower_amps, call, capacity, delta_e, delta_t,
                                                                    error, inducer_amps, run_time))


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

