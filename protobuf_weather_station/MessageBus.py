# SPDX-FileCopyrightText: 2021 phearzero for Telluric Guru
# SPDX-License-Identifier: MIT
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as mqtt


class MessageBus:
    def __init__(self, esp, secrets):
        def connected(client, userdata, flags, rc):
            print("  🏤 Connected to MQTT, Listening for topic changes on %s" % secrets['feed'])
            client.subscribe(secrets['feed'])

        def disconnected(client, userdata, rc):
            print("  🏤 Disconnected from MQTT!")

        def message(client, topic, msg):
            print("✉️ New message on topic {0}: {1}".format(topic, msg))

        # Initialize MQTT interface with the esp interface
        mqtt.set_socket(socket, esp)

        # Set up a MiniMQTT Client
        self.client = mqtt.MQTT(
            secrets["broker"],
            secrets["port"]
        )

        # Setup the callback methods above
        self.client.on_connect = connected
        self.client.on_disconnect = disconnected
        self.client.on_message = message

    def connect(self):
        # Connect the client to the MQTT broker.
        print("  🏤 Connecting to MQTT...")
        self.client.connect()
