import ssl
import wifi
import socketpool
import adafruit_requests
import board
import busio
import displayio
import adafruit_displayio_ssd1306
from secrets import secrets
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import adafruit_minimqtt.adafruit_minimqtt as MQTT

wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
## Now connected to wifi!

displayio.release_displays()
oled_reset = board.D0

# Use for I2C
i2c = busio.I2C(board.SCL1,board.SDA1)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d, reset=oled_reset)

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 3

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

font = bitmap_font.load_font("font/Helvetica-Bold-16.bdf")
# Time Label
# time_area = label.Label(
#     font, text="", color=0xFFFFFF, x=WIDTH - BORDER - 46, y=HEIGHT - 14
# )
# splash.append(time_area)
# Sensor Label
sensor_area = label.Label(
    font, text="Work Status", color=0xFFFFFF, x=8, y= 14
)
splash.append(sensor_area)
# Litterbox counter label
work_status_area = label.Label(
    font, text="", color=0xFFFFFF, x=8, y=HEIGHT - 14
)
splash.append(work_status_area)


## manage connection to Home Assistant
# time_topic = "system/time"
work_topic = "work/meeting"
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name


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


def message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print("Topic {0}: {1}".format(topic, message))


def work_message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print("Topic {0}: {1}".format(topic, message))
    if topic == work_topic:
        if message == "on":
            work_status_area.text = "In a Meeting"
        elif message == "off":
            work_status_area.text = "Free"


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    port=secrets["mqtt_port"],
    username=secrets["mqtt_username"],
    password=secrets["mqtt_password"],
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
mqtt_client.on_message = message


mqtt_client.add_topic_callback(work_topic, work_message)

print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()

mqtt_client.subscribe(work_topic)


while True:
    try:
        mqtt_client.loop(timeout=0.3)
    except MemoryError as e:
        pass
    except Exception as e:
        print(e)
