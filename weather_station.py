from gpiozero import Button
import time
import math
import bme688_sensor
import wind_direction_byo
import statistics
import ds18b20_therm
import database
import socket

wind_count = 0  # Counts how many half-rotations
radius_cm = 9.0  # Radius of your anemometer
wind_interval = 5  # How often (secs) to report speed
interval = 300

ANEMOMETER_FACTOR = 1.18
BUCKET_SIZE = 0.2794

store_speeds = []
store_directions = []


# Every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count = wind_count + 1
    # print("spin" + str(wind_count))


def reset_wind():
    global wind_count
    wind_count = 0


# Calculate the wind speed
def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0

    dist_km = (circumference_cm * rotations) / 100000

    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * 3600

    return km_per_hour * ANEMOMETER_FACTOR


def bucket_tipped():
    global rain_count
    rain_count = rain_count + 1
    # print (rain_count * BUCKET_SIZE)


def reset_rainfall():
    global rain_count
    rain_count = 0


wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin
rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped
# temp_probe = ds18b20_therm.DS18B20()


# For use when ground temp probe is connected to another device
# See: https://gist.github.com/stmio/658f5dd1a6b3d24d7b4ecf526f68ce21
def get_ground_temp(ip="192.168.1.155", port=42800):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    data = sock.recv(1024).decode()
    sock.close()
    return data


db = database.weather_database()

while True:
    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
        # time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction_byo.get_value())

        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    wind_average = wind_direction_byo.get_average(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)
    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()
    store_speeds = []
    store_directions = []
    # ground_temp = temp_probe.read_temp()
    ground_temp = get_ground_temp()
    ambient_temp, pressure, humidity = bme688_sensor.read_all()

    db.insert(
        ambient_temp,
        ground_temp,
        0,
        pressure,
        humidity,
        wind_average,
        wind_speed,
        wind_gust,
        rainfall,
    )
    print(
        wind_average,
        wind_speed,
        wind_gust,
        rainfall,
        humidity,
        pressure,
        ambient_temp,
        ground_temp,
    )
