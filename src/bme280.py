#!/usr/bin/env python
from smbus2 import SMBus
from RPi.bme280 import bme280

class SensorBME280():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    def getValue(self):
        calibration_params = bme280.load_calibration_params(self.bus, self.address)
        val = bme280.sample(self.bus, self.address, calibration_params)
        return val
