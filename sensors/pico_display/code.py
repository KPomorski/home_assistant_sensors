"""
adapted from http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
"""

import os
import ipaddress
import wifi
import socketpool
import board
import ssl
import microcontroller
import adafruit_requests
import time
import terminalio
import displayio
from digitalio import DigitalInOut, Direction, Pull
import busio
from adafruit_display_text import label
from adafruit_st7789 import ST7789

print("Connecting to WiFi")
#  connect to your SSID
wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

# Release any resources currently in use for the displays
displayio.release_displays()
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)

print("==============================")
print(os.uname())
print("Hello Raspberry Pi Pico/CircuitPython ST7789 SPI IPS Display")
print()

led_r = DigitalInOut(board.GP6)
led_b = DigitalInOut(board.GP7)
led_g = DigitalInOut(board.GP8)

buttons = []
button_pins = [
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15
]

for pin in button_pins:
    button_pin = DigitalInOut(pin)
    button_pin.direction = Direction.INPUT
    button_pin.pull = Pull.UP
    buttons.append(button_pin)

tft_cs = board.GP17
tft_dc = board.GP16
backlight = board.GP20

# display_bus = displayio.FourWire(spi, chip_select=tft_cs, command=tft_dc, reset=tft_res)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(display_bus, rotation=180, width=135, height=240, rowstart=40, colstart=53, backlight_pin=backlight)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(135, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(133, 238, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x0000FF
inner_sprite = displayio.TileGrid(inner_bitmap,
                                  pixel_shader=inner_palette, x=1, y=1)
splash.append(inner_sprite)

# Draw a label
text_group1 = displayio.Group(scale=1, x=20, y=40)
text1 = "gaussisbauss"
text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFF0000)
text_group1.append(text_area1)  # Subgroup for text scaling
# Draw a label
text_group2 = displayio.Group(scale=1, x=20, y=60)
text2 = "CircuitPython"
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF)
text_group2.append(text_area2)  # Subgroup for text scaling

# Draw a label
text_group3 = displayio.Group(scale=1, x=20, y=100)
text3 = "Sup"
text_area3 = label.Label(terminalio.FONT, text=text3, color=0x0000000)
text_group3.append(text_area3)  # Subgroup for text scaling
# Draw a label
text_group4 = displayio.Group(scale=2, x=20, y=120)
text4 = "Yo dog"
text_area4 = label.Label(terminalio.FONT, text=text4, color=0x000000)
text_group4.append(text_area4)  # Subgroup for text scaling

splash.append(text_group1)
splash.append(text_group2)
splash.append(text_group3)
splash.append(text_group4)

rot = 0
while True:
    if not buttons[0].value:
        print("Button a Pressed")
    if not buttons[1].value:
        print("Button b Pressed")
    if not buttons[2].value:
        print("Button x Pressed")
    if not buttons[3].value:
        print("Button y Pressed")
    # if button_a.read():                                   # if a button press is detected then...
    #     displayio.release_displays()                      # clear to black
    #     text4 = "Button A pressed"                        # display some text on the screen
    #     time.sleep(1)                                     # pause for a sec
    #     displayio.release_displays()                      # clear to black again
    # elif button_b.read():
    #     displayio.release_displays()
    #     text4 = "Button B pressed"
    #     time.sleep(1)
    #     displayio.release_displays()
    # elif button_x.read():
    #     displayio.release_displays()
    #     text4 = "Button X pressed"
    #     time.sleep(1)
    #     displayio.release_displays()
    # elif button_y.read():
    #     displayio.release_displays()
    #     text4 = "Button Y pressed"
    #     time.sleep(1)
    #     displayio.release_displays()
    # else:
    #     text4 = "Press any button!"
    # time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
    pass
    # time.sleep(5.0)
    # rot = rot + 90
    # if (rot>= 360):
    #     rot= 0
    # display.rotation = rot
