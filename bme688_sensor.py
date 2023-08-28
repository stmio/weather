import bme280
import smbus2
from time import sleep

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280_load_calibration_params(bus, address)


def read_all():
    bme280_data = bme.sample(bus, address)
    return bme280_data.humidity, bme280_data.pressure, bme280_data.temperature
