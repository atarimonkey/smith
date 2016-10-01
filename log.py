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


# last_error = ''


class Log:
    """This class is to facilitate the logging of measurements or errors in each of your modules.
    It can log to files and/or to the phant web service"""

    def __init__(self, logname):
        """This defines the name of the logger and the file that will be logged to."""
        assert type(logname) is str, "Invalid Log Name"
        self.file_log_cache = {}
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(logging.INFO)
        self.log_file = logging.handlers.RotatingFileHandler("{0}.log".format(logname), maxBytes=10485760,
                                                             backupCount=1)
        self.log_file.setLevel(logging.INFO)
        self.logger.addHandler(self.log_file)
        self.file_formatter = logging.Formatter('%(asctime)s  %(name)s:%(levelname)s: %(message)s',
                                                datefmt='%Y/%m/%d %H:%M:%S')
        self.log_file.setFormatter(self.file_formatter)
        self.web_logger = phant.Phant('2JrDOrmOnxt3KK1dGW1b', 'bloweramps', 'call', 'capacity', 'deltae', 'deltat',
                                      'error', 'induceramps', 'runtime', private_key='GP8ME8GEoyCvNN2x0z27')
        with open('error_code.json', 'r') as f:
            self.error_codes = json.load(f)

    def clean_cache(self):
        """Removes old cache entries"""
        old_data = []
        assert type(self.file_log_cache) is dict, "Invaled cache data"
        for log_message in self.file_log_cache:
            if self.file_log_cache[log_message] + 86400 < time.time():
                old_data.append(log_message)

        for data in old_data:
            self.file_log_cache.pop(data)

    def log_to_file(self, blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time):
        """Log a message to a log file using the name defined at creation, logname.log."""
        error_message = -1
        message = "Runtime={7}, Delta T={4}, Inducer Amps={6}, Error={5:02}, Delta E={3}, Call={1}, " \
                  "Blower Amps={0}, Capacity={2}, Message={8}".format(blower_amps, call, capacity, delta_e, delta_t,
                                                         error, inducer_amps, run_time, self.error_codes[str(error)])
        assert type(message) is str, "Invalid log data"

        start_index = message.find("Error=")
        if start_index > -1:
            error_message = int(message[start_index + 6: start_index + 8])
        self.clean_cache()
        if message not in self.file_log_cache:
            if -1 < error_message < 7:
                self.file_log_cache[message] = time.time()
            self.logger.info(message)

    def log_to_web(self, blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time):
        """Log data to the phant web service."""
        self.web_logger.log(blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time)

    def log_to_all(self, blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time):
        """Log data to phant and the defined log file"""
        self.log_to_web(blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time)
        self.log_to_file(blower_amps, call, capacity, delta_e, delta_t, error, inducer_amps, run_time)

# def clear_log():
#     os.remove('log')
#
# def entry(c, rt, ba, ia, dt, de, cap):
#     _ = StructuredMessage
#     p = phant.Phant('2JrDOrmOnxt3KK1dGW1b', 'Call', 'Error', 'Run Time', 'Blower Amps', 'Inducer Amps', 'Delta T', 'Delta E', 'capacity', privatekey = 'GP8ME8GEoyCvNN2x0z27')
#     logging.basicConfig(filename='log', level=logging.INFO, format='%(asctime)-15s %(message)s')
#     logging.info(_(c, run_time= rt, blower_amps= ba, inducer_amps= ia,
#                  delta_T= dt, delta_E= de, capacity= cap ))
#     p.log(c, 'None', rt, ba, ia, dt, de, cap)
#
# def error(c, e, rt, ba, ia, dt, de, cap, warning):
#     # this may need to be simplified
#     global last_error
#     t2 = time.time()
#     p = phant.Phant('2JrDOrmOnxt3KK1dGW1b', 'Call', 'Error', 'RunTime', 'BlowerAmps', 'InducerAmps', 'DeltaT', 'DeltaE', 'capacity', privatekey = 'GP8ME8GEoyCvNN2x0z27')
#
#     if last_error == '' or (t2 - last_error) >= 86400:
#         #email a warning
#         warning
#         last_error = t2
#
#     logging.basicConfig(filename='log.error', level=logging.ERROR, format='%(asctime)-15s %(message)s')
#     logging.error(_(c, error= e, run_time= rt, blower_amps= ba, inducer_amps= ia,
#                  delta_T= dt, delta_E= de ))
#     p.log(c, e, rt, ba, ia, dt, de, cap)
#
# class StructuredMessage(object):
#     def __init__(self, message, **kwargs):
#         self.message = message
#         self.kwargs = kwargs
#
#     def __str__(self):
#         return '%s >>> %s' % (self.message, json.dumps(self.kwargs))
#
#
#
# def main():
# 	print 'test'
# 	return 0
#
# if __name__ == '__main__':
# 	main()
