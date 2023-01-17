import requests
import os
from dotenv import main as dotenv


dotenv.load_dotenv()
HA_API_URL = os.getenv("HA_API_URL")
HA_TOKEN = os.getenv("HA_API_TOKEN")


def trigger_service(service, data):
    # service = "light/toggle"
    # data = {"entity_id": "light.floor_light"}
    request_url = HA_API_URL + "/services/" + service
    headers = {"Authorization": "Bearer {}".format(HA_TOKEN)}
    response = requests.post(request_url, headers=headers, json=data)
    response.close()


# Handle a button press
def button_press(button_label):
    print("button pressed")
    if button_label == 'a':
        service = "light/toggle"
        data = {"entity_id": "light.floor_light"}
    elif button_label == 'b':
        service = "switch/toggle"
        data = {"entity_id": "switch.bedside_light"}
    trigger_service(service, data)


