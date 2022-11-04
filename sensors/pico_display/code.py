"""
adapted from http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
"""

import os
import board
import time
import terminalio
import displayio
import busio
from adafruit_display_text import label
import adafruit_st7789
from pico_display import Button, RGBLED


print("==============================")
print(os.uname())
print("Hello Raspberry Pi Pico/CircuitPython ST7789 SPI IPS Display")
print(adafruit_st7789.__name__ + " version: " + adafruit_st7789.__version__)
print()

# Release any resources currently in use for the displays
displayio.release_displays()

led = RGBLED(board.GP6, board.GP7, board.GP8)

button_a = Button(board.GP12)
button_b = Button(board.GP13)
button_x = Button(board.GP14)
button_y = Button(board.GP15)

tft_cs = board.GP17
tft_dc = board.GP16
#tft_res = board.GP23
spi_mosi = board.GP19
spi_miso = board.GP20
spi_clk = board.GP18

"""
classbusio.SPI(clock: microcontroller.Pin,
                MOSI: Optional[microcontroller.Pin] = None,
                MISO: Optional[microcontroller.Pin] = None)
"""
displayio.release_displays()
spi = busio.SPI(spi_clk, MOSI=spi_mosi, MISO=spi_miso)

#display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_res)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
#I get the parameters by guessing and trying
#display = ST7789(display_bus, width=135, height=240, rowstart=40, colstart=53)
display = adafruit_st7789.ST7789(display_bus,
                                 width=135, height=240,
                                 rowstart=40, colstart=53)
display.rotation = 180
# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(135, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette, x=0, y=0)
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
text3 = adafruit_st7789.__name__
text_area3 = label.Label(terminalio.FONT, text=text3, color=0x0000000)
text_group3.append(text_area3)  # Subgroup for text scaling
# Draw a label
text_group4 = displayio.Group(scale=2, x=20, y=120)
text4 = adafruit_st7789.__version__
text_area4 = label.Label(terminalio.FONT, text=text4, color=0x000000)
text_group4.append(text_area4)  # Subgroup for text scaling

splash.append(text_group1)
splash.append(text_group2)
splash.append(text_group3)
splash.append(text_group4)

time.sleep(3.0)

rot = 0
while True:
    if button_a.read():                                   # if a button press is detected then...
        displayio.release_displays()                      # clear to black
        text4 = "Button A pressed"                        # display some text on the screen
        time.sleep(1)                                     # pause for a sec
        displayio.release_displays()                      # clear to black again
    elif button_b.read():
        displayio.release_displays()
        text4 = "Button B pressed"
        time.sleep(1)
        displayio.release_displays()
    elif button_x.read():
        displayio.release_displays()
        text4 = "Button X pressed"
        time.sleep(1)
        displayio.release_displays()
    elif button_y.read():
        displayio.release_displays()
        text4 = "Button Y pressed"
        time.sleep(1)
        displayio.release_displays()
    else:
        text4 = "Press any button!"
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses

#     time.sleep(5.0)
#     rot = rot + 90
#     if (rot>=360):
#         rot =0
#     display.rotation = rot
