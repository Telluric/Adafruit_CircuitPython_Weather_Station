# SPDX-FileCopyrightText: 2021 phearzero for Telluric Guru
# SPDX-License-Identifier: MIT

"""Network API for Weather Station"""
import board
import busio
import neopixel
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager


class Network:
    def __init__(self, secrets):
        # AirLift FeatherWing Pins
        esp32_cs = DigitalInOut(board.D13)
        esp32_ready = DigitalInOut(board.D11)
        esp32_reset = DigitalInOut(board.D12)

        # ESP32 API
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

        # Set NeoPixel to Wifi Status
        status_light = neopixel.NeoPixel(
            board.NEOPIXEL, 1, brightness=0.2
        )

        # Wifi manager
        self.wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(self.esp, secrets, status_light)

    def connect(self):
        # Connect to WiFi
        print("  📶 Connecting to WiFi...")
        self.wifi.connect()
        print("  📶 Connected to", str(self.esp.ssid, "utf-8"), "\tRSSI:", self.esp.rssi)
        print("  📶 My IP address is", self.esp.pretty_ip(self.esp.ip_address))
