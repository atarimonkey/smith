#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  alerts.py
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

__author__ = 'David'

import smtplib
import time


def alert(owners_email, contractors_email, message):
    server = 'smtp.gmail.com'
    port = 587

    sender = 'HVACbot@gmail.com'
    recipient = owners_email, contractors_email
    password = ''
    subject = 'alert from your HVACbot'
    body = message

    body = "" + body + ""
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    session = smtplib.SMTP(server, port)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(sender, password)
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def warning_maint(owner, contractor, system, contractor_info):
    message = "Your " + system + " is in need of maintenance.\rPlease call.\r" + contractor_info + "\rThank You\rHVACbot"
    alert(owner, contractor, message)


def warning_blower(owner, contractor, contractor_info):
    message = ["HVACbot has detected a issue with your blower motor.\r",
               "Possible causes are:\r",
               "Weak Capacitor\r",
               "Bad Blower Motor\r",
               "Loose or Bad connection\r",
               "Bad Control Board\r",
               "Please Call.\r" + contractor_info,
               "\rThank you\rHVACbot"]
    alert(owner, contractor, message)


def warning_inducer(owner, contractor, contractor_info):
    message = ["HVACbot has detected a issue with your inducer motor.\r",
               "Please Contact\r" + contractor_info,
               "\rThank you\rHVACbot"]
    alert(owner, contractor, message)


def warning_flame_sensor(owner, contractor, contractor_info):
    message = ["HVACbot has detected a issue with your inducer motor.\r",
               "Please Contact\r" + contractor_info,
               "\rThank you\rHVACbot"]
    alert(owner, contractor, message)


def warning_ignition(owner, contractor, contractor_info):
    message = ["HVACbot has detected ignition failure.\r",
               "Possible causes are:\r",
               "HSI failure,\r",
               "Gas valve failure,\r",
               "clogged flue,\r",
               "Stuck Pressure Switch,\r",
               "Loose connection,\r",
               "Bad Control Board,\r",
               "Please contact,\r" + contractor_info,
               "\rThank you\rHVACbot"]
    alert(owner, contractor, message)


def warning_temp_rise(owner, contractor, contractor_info):
    message = ["HVACbot has detected a high temperature.\r",
               "Possible causes are:\r",
               "Clogged filter,\r",
               "Blocked vent,\r",
               "Clogged Coil,\r",
               "Please contact,\r" + contractor_info,
               "\rThank you\rHVACbot"]
    alert(owner, contractor, message)


def warning_temp_drop(owner, contractor, contractor_info):
    message = ["HVACbot has detected a high temperature.\r",
               "Possible causes are:\r",
               "Clogged filter,\r",
               "Blocked vent,\r",
               "Clogged Coil,\r",
               "Low charge,\r",
               "Please contact,\r" + contractor_info,
               "\rThank you\rHVACbot"]
    alert(owner, contractor, message)


def warning_low_cap(owner, contractor, contractor_info):
    message = {"HVACbot has detected a problem with your air conditioner.\r",
               "Possible refrigerant issues.\r",
               "Please contact,\r" + contractor_info,
               "\rThank you,\rHVACbot"}
    alert(owner, contractor, message)




def main():
	
	return 0

if __name__ == '__main__':
	main()

