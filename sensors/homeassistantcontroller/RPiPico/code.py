import os
import time
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import digitalio
from adafruit_debouncer import Button


api_url = os.getenv("HA_API_URL")
token = os.getenv("HA_BEARER_TOKEN")


pin = digitalio.DigitalInOut(board.GP15)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UPe

#  connect to SSID
wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


#  Triggers a Home Assistant Service
def trigger_service():
    request_url = api_url + "/services/light/toggle"
    headers = {"Authorization": "Bearer {}".format(token)}
    data = {"entity_id": "light.floor_light"}
    response = requests.post(request_url, headers=headers, json=data)
    response.close()


# Handle a button press
def button_press():
    print("button pressed")
    trigger_service()


# Main program loop
while True:
    button.update()
    if button.pressed:
        button_press()

