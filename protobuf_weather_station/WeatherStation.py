# SPDX-FileCopyrightText: 2021 phearzero for Telluric Guru
# SPDX-License-Identifier: MIT

from .Network import Network
from .MessageBus import MessageBus
from .Observations import Observations

print(('-' * 40) + 'Weather-Station-IO' + ('-' * 40))
print('⛈️ Booting Weather Station Node - https://weather.telluric.guru')
print('📝 Weather Station is under the MIT License - https://opensource.org/licenses/MIT')
print('💖 Special Thanks to ladyada for making this possible!')
print(('-' * 98))

NaN = float("NaN")


class WeatherStation:
    # Sensor AVG Data
    temperature = 0
    humidity = 0
    altitude = 0
    gas = 0
    pressure = 0
    sea_level_pressure = 0

    """Create a new Weather Station with Observations, Network and MessageBus"""

    def __init__(self, secrets):
        print('✨ Creating a new WeatherStation()')
        self.secrets = secrets
        self.net = Network(secrets)
        self.bus = MessageBus(self.net.esp, secrets)
        self.observe = Observations(self.bus, self.secrets, self.observation)

    def __repr__(self):
        return "WeatherStation({secrets})"

    def __str__(self):
        return (
            f"    🌡️\tTemperature: {self.temperature}\n"
            f"    💦\tHumidity: {self.humidity}\n"
            f"    ☠️\tGas: {self.gas}\n"
            f"    ⬇️\tPressure: {self.pressure}\n"
            f"    🧭\tAltitude: {self.altitude}"
        )

    def connect(self):
        print('⚙️ Connecting Weather Station')
        self.net.connect()
        self.bus.connect()

    def observation(self, obs):
        self.temperature = obs['temperature']
        self.humidity = obs['humidity']
        self.altitude = obs['altitude']
        self.gas = obs['gas']
        self.pressure = obs['pressure']
        self.sea_level_pressure = obs['sea_level_pressure']

    def loop(self):
        print('➰ Running Loop')
        self.bus.client.loop()
        self.observe.loop()
        print(self)
