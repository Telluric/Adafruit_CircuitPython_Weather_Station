# SPDX-FileCopyrightText: 2021 phearzero for Telluric Guru
# SPDX-License-Identifier: MIT

import time
import board
import analogio
import adafruit_bme680
from simpleio import map_range
from minipb import Wire

buffer = Wire((
    ('temperature', 'f'),
    ('altitude', 'f'),
    ('sea_level_pressure', 'f'),
    ('replicates', 'f'),
    ('pressure', 'f'),
    ('intervals', 'f'),
    ('gas', 'f'),
    ('humidity', 'f'),
    ('wind_speed', 'f'),
    ('timestamp', 'f'),
))

# anemometer defaults
anemometer_min_volts = 0.4
anemometer_max_volts = 2.0
min_wind_speed = 0.0
max_wind_speed = 32.4

def adc_to_wind_speed(val):
    """Returns anemometer wind speed, in m/s.
    :param int val: ADC value
    """
    voltage_val = val / 65535 * 3.3
    return map_range(voltage_val, 0.4, 2, 0, 32.4)

i2c = board.I2C()  # uses board.SCL and board.SDA


class Observations:
    # Interval Checks
    interval = 900000  # Real 15 Min
    interval_start = 0

    # Sensor Data
    temperature = []
    humidity = []
    altitude = []
    gas = []
    pressure = []
    wind_speed = []

    # Sensor API
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    # Analog Input
    adc = analogio.AnalogIn(board.A1)

    def __init__(self, bus, secrets, callback):
        print('✨ Creating a new Observations Interface()')
        self.interval_start = Observations.get_time()
        self.secrets = secrets
        self.bus = bus
        self.callback = callback

    def __str__(self):
        return buffer.encode({
            'temperature': self.temperature[0],
            'humidity': self.humidity[0],
            'altitude': self.altitude[0],
            'gas': self.gas[0],
            'pressure': self.pressure[0],
            'sea_level_pressure': self.sensor.sea_level_pressure,
            'wind_speed': self.wind_speed[0]
        })

    @staticmethod
    def get_time():
        return round(time.time() * 1000)

    def averages(self, timestamp):
        res = {
            "timestamp": timestamp,
            "replicates": 1,
            "intervals": len(self.temperature),
            "temperature": sum(self.temperature) / len(self.temperature),
            "gas": sum(self.gas) / len(self.gas),
            "humidity": sum(self.humidity) / len(self.humidity),
            "pressure": sum(self.pressure) / len(self.pressure),
            "altitude": sum(self.altitude) / len(self.altitude),
            "sea_level_pressure": self.sensor.sea_level_pressure,
            "wind_speed": sum(self.wind_speed)/len(self.wind_speed)
        }
        self.temperature.clear()
        self.humidity.clear()
        self.gas.clear()
        self.pressure.clear()
        self.altitude.clear()
        self.wind_speed.clear()
        return res

    def loop(self):
        print('  ✨ Observation Loop')
        self.callback({
            "temperature": self.sensor.temperature,
            "humidity": self.sensor.humidity,
            "gas": self.sensor.gas,
            "pressure": self.sensor.pressure,
            "altitude": self.sensor.altitude,
            "sea_level_pressure": self.sensor.sea_level_pressure,
            "wind_speed": adc_to_wind_speed(self.adc.value)
        })
        if self.interval_start + self.interval < Observations.get_time():
            self.interval_start = Observations.get_time()
            avgs = self.averages(self.interval_start)
            self.bus.client.publish(self.secrets['buffer'], buffer.encode(avgs))
        self.temperature.append(self.sensor.temperature)
        self.humidity.append(self.sensor.humidity)
        self.gas.append(self.sensor.gas)
        self.pressure.append(self.sensor.pressure)
        self.altitude.append(self.sensor.altitude)
        self.wind_speed.append(adc_to_wind_speed(self.adc.value))
