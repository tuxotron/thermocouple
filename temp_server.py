#!/usr/bin/env python
import web
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

# Raspberry Pi software SPI configuration.
#CLK = 25
#CS  = 24
#DO  = 18
#sensor = MAX31855.MAX31855(CLK, CS, DO)

# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 0
sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

urls = (
	'/', 'index',
	'/temperature', 'temperature'
)

app = web.application(urls, globals())

class index:
	def GET(self):
		try:
			f = open('/home/pi/index.html', 'r')
			return f.read()
		except:
			return 'Not found'

class temperature:
	def GET(self):
		external = sensor.readTempC()
		internal = sensor.readInternalC()
		output = '"external": {0:0.3F}, \r "internal": {1:0.3F}'.format(external, internal)
		web.header('Content-Type', 'application/json')
		return '{\r' + output + '\r}'

if __name__ == "__main__":
	app.run()
