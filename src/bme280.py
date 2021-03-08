import smbus2
import bme280

class bme280();
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    def getValues(self):
        calibration_params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, calibration_params)
