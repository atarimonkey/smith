#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bme280.py
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
import smbus, time

class BME280(self):
	
	def __init__(bus_number, i2c_address):
		self.bus_number = bus_number
		self.i2c_address = i2c_address
	
	self.bus = smbus.SMbus(self.bus_address)
	
	self.digT = []
	self.digH = []
	self.digP = []
	
	self.t_fine = 0.0
	
	def writeReg(self, reg_address, data):
		self.bus.write_byte_data(self.i2c_address, reg_address, data)
	
	def get_calib_param(self):
		calib = []
		for i in range(0x88, 0x88+24):
			calib.append(self.bus.read_byte_data(self.i2c_address, i ))
		calib.append(self.bus.read_byte_data(self.i2c_address, 0xA1))
		for i in range(0xE1, 0xE1+7):
			calib.append(self.bus.read_byte_data(self.i2c_address, i))
		
		self.digT.append((calib[1] << 8) | calib[0])
		self.digT.append((calib[3] << 8) | calib[2])
		self.digT.append((calib[5] << 8) | calib[4])
		self.digP.append((calib[7] << 8) | calib[6])
		self.digP.append((calib[9] << 8) | calib[8])
		self.digP.append((calib[11] << 8) | calib[10])
		self.digP.append((calib[13] << 8) | calib[12])
		self.digP.append((calib[15] << 8) | calib[14])
		self.digP.append((calib[17] << 8) | calib[16])
		self.digP.append((calib[19] << 8) | calib[18])
		self.digP.append((calib[21] << 8) | calib[20])
		self.digP.append((calib[23] << 8) | calib[22])
		self.digH.append(calib[24])
		self.digH.append((calib[26] << 8) | calib[25])
		self.digH.append(calib[27])
		self.digH.append((calib[28] << 4) | (0x0F & calib[29]))
		self.digH.append((calib[30] << 4) | ((calib[29] >> 4) & 0x0F))
		self.digH.append(calib[31])
		
		for i in range(1, 2):
			if self.digT[i] & 0x8000:
				self.digT[i] = (-self.digT[i] ^ 0xFFFF) + 1
				
		for i in range(1, 8):
			if self.digP[i] & 0x8000:
				self.digP[i] = (-self.digP[i] ^ 0xFFFF) + 1
				
		for i in range(0, 6):
			if self.digH[i] & 0x8000:
				self.digH[i] = (-self.digH[i] ^ 0xFFFF) + 1
	
	def readData(self, thp):
		data = []
		
		for i in range(0xF7, 0xF7+8):
			data.append(self.bus.read_byte_data(self.i2c_address, i)
			
		pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
		temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
		hum_raw = (data[6] << 8) | data[7]
		
		t = compensate_T(temp_raw)
		p = compensate_P(pres_raw)
		h = compensate_H(hum_raw)
		
		if thp == 't':
			return t
		elif thp == 'p':
			return p
		elif thp == 'h':
			return h
		else:
			print "error"
			pass
		
	def compensate_P(self, adc_P):
		pressure = 0.0
		
		v1 = (self.t_fine / 2.0) - 64000.0
		v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048.0) * digP[5]
		v2 = ((v1 * digP[4]) * 2.0)
		v2 = (v2 / 4.0) + (digP[3] * 65536.0)
		v1 = (((digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192.0)) / 8.0) + ((digP[1] * v1) / 2.0)) / 262144.0
		v1 = ((32768.0 + v1) * digP[0]) / 32768.0
		
		if v1 == 0:
			return 0
		pressure = ((1048576.0 - adc_P) - (v2 / 4096.0)) * 3125.0
		if pressure < 0x80000000:
			pressure = (pressure * 2.0) / v1
		else:
			pressure = (pressure / v1) * 2.0
		v1 = (digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096.0
		v2 = ((pressure / 4.0) * digP[7]) / 8192.0
		pressure = pressure + ((v1 + v2 + digP[6]) / 16.0)
		
		print "pressure : %7.2f hPa" % (pressure / 100)
		return (pressure / 100)
		
	def compensate_T(self, adc_T):
		v1 = (adc_T / 16384.0 - digT[0] / 1024.0) * digT[1]
		v2 = (adc_T / 131072.0 - digT[0] / 8192.0) *(adc_T / 131072.0 - digT[0] / 8192.0) * digT[2]
		self.t_fine = v1 + v2
		temperature = self.t_fine / 5120.0
		
		print "temp : %-6.2f c" % (tempurature)
		return tempurature
		
	def compensate_H(self, adc_H):
		var_h =self.t_fine - 76800.0
		if var_h != 0:
			var_h = (adc_H - (digH[3] * 64.0 + digH[4] / 16384.0 * var_h)) * (digH[1] / 65536.0 * (1.0 + digH[5] / 67108864.0 * var_h * (1.0 + digH[2] / 67108864.0 * var_h)))
		else:
			return 0
		
		var_h = var_h * (1.0 - digH[0] * var_h / 524288.0
		
		if var_h > 100:
			var_h = 100.0
		elif var_h < 0.0:
			var_h = 0.0
			
		print "hum: %6.2f %" % (var_h)
		return var_h
		
	def setup(self):
		osrs_t = 1
		osrs_p = 1
		osrs_h = 1
		mode = 3
		t_sb = 5
		filter = 0
		spi3w_en = 0
		
		ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
		config_reg = (t_sb << 5) | (filter << 2) | spi3w_en
		ctrl_hum_reg = osrs_h
		
		writeReg(0xF2, ctrl_hum_reg)
		writeReg(0xF4, ctrl_meas_reg)
		writeReg(0xF5, config_reg)
		
	


def main():
	
	return 0

if __name__ == '__main__':
	main()

