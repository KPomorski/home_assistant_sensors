# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, and some white text.
"""

import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

def initialize_display():
    displayio.release_displays()

    oled_reset = board.D0

    # Use for I2C
    i2c = busio.I2C(board.SCL1,board.SDA1)
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3d, reset=oled_reset)


    WIDTH = 128
    HEIGHT = 64  # Change to 64 if needed
    BORDER = 5

    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
