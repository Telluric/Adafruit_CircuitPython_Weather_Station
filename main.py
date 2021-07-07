"""Protobuf Weather Station"""
import time
from protobuf_weather_station import WeatherStation

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

ws = WeatherStation(secrets)
ws.connect()

while True:
    ws.loop()
    time.sleep(2)
