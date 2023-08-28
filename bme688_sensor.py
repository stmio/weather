import bme680
import time

sensor = bme680.BME680()


def read_all():
    while True:
        if sensor.get_sensor_data():
            return sensor.data.temperature, sensor.data.pressure, sensor.data.humidity

        time.sleep(1)


# Original code for BME280 (new code is for BME68x):

# import bme280
# import smbus2
# port = 1
# address = 0x76
# bus = smbus2.SMBus(port)
# bme280_load_calibration_params(bus, address)
# def read_all():
#     bme280_data = bme.sample(bus, address)
#     return bme280_data.humidity, bme280_data.pressure, bme280_data.temperature
