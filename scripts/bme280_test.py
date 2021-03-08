#!/usr/bin/env python
import smbus2
import bme280

class sensorBME280():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    def getValue(self):
        calibration_params = bme280.load_calibration_params(self.bus, self.address)
        val = bme280.sample(self.bus, self.address, calibration_params)
        return val

sensor = sensorBME280()
data = sensor.getValue()
print(data.temperature)
print(data.pressure)
print(data.humidity)
