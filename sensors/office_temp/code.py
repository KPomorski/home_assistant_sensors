# SPDX-FileCopyrightText: 2022 Taxelas
# SPDX-License-Identifier: MIT
"""
python script to read mcp9808 temperature and publish it in mqtt.
Using discovery topic to create entity in Home Assistant.
"""
import ssl
import socketpool
import wifi
import time
import json
from array import array
import board
import busio
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import ulab.numpy as np
import adafruit_mcp9808
from secrets import secrets


i2c = busio.I2C(board.SCL1, board.SDA1)
# i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller


# To initialise using the default address:
mcp = adafruit_mcp9808.MCP9808(i2c)

# Set up internet connection
wifi.radio.connect(secrets["ssid"], secrets["password"])
# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
# Set up a MiniMQTT Client
client = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    port=secrets["mqtt_port"],
    username=secrets["mqtt_username"],
    password=secrets["mqtt_password"],
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)
client.connect()

# Create autodiscovery topic for Home assistant
# "homeassistant" is autodiscovery prefix in home assistant
send_msg = {
    "state_topic": "homeassistant/sensor/sensorOfficeTemp/state",
    "device_class": "temperature",
    "unit_of_measurement": "°F",
    "value_template": "{{ value_json.temperature }}",
    "device": {
        "identifiers": ["esp32sensorgatewayn01"],
        "manufacturer": "Adafruit",
        "model": "QtPy ESP32-S2",
        "name": "Office temperature",
        "sw_version": "MCU9808",
    },
    "name": "Office temperature",
    "unique_id": "esp32sensorgateway_0x01",
}
client.publish(
    "homeassistant/sensor/sensorOfficeTemp/config",
    msg=json.dumps(send_msg),
    qos=0,
    retain=True,
)  # publish
temp1m = np.zeros(9)  # using array to aproximate 10 temperature readings
avgtemp = 0
while True:
    # when we've filled up the array, replace values
    for count in range(0, 9):
        temperature_fahrenheit = mcp.temperature * 9 / 5 + 32
        temp1m[count] = temperature_fahrenheit
        print("Temperature: {} F ".format(temperature_fahrenheit))
        print(temp1m)
        time.sleep(10)
    avgtemp = round(np.mean(temp1m), 1)
    print("avgtemp {} F".format(avgtemp))
    send_msg = {"temperature": avgtemp}
    print('Sending {}'.format(send_msg))
    client.publish(
        "homeassistant/sensor/sensorOfficeTemp/state",
        msg=json.dumps(send_msg)
    )  # publish result in mqtt
