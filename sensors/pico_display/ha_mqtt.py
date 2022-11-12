import os
import adafruit_minimqtt.adafruit_minimqtt as MQTT


def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(mqtt_client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))


# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(broker=os.getenv('HA_BROKER'),
                        username=os.getenv('HA_MQTT_USER'),
                        password=os.getenv('HA_MQTT_PW'),
                        port=1883)

topics = ['sensor/status/pico_dislplay',
          'work/meeting',
          'sensor/button/pico_display/a',
          'sensor/button/pico_display/b',
          'sensor/button/pico_display/x',
          'sensor/button/pico_display/y']
status_topic = topics[0]


# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
mqtt_client.on_message = message

print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()

for i in range(topics):
    print("Subscribing to %s" % topics[i])
    mqtt_client.subscribe(topics[i])
print("Publishing to %s" % status_topic)
mqtt_client.publish(status_topic, "Hello Broker!")

while True:
    try:
        mqtt_client.loop(timeout=0.3)
    except MemoryError as e:
        pass
    except Exception as e:
        print(e)
