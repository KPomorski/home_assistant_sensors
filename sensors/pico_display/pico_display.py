import board
import time
from digitalio import DigitalInOut, Direction, Pull
import pwmio as PWM


class Button:
    def __init__(self, button, invert=True, repeat_time=200, hold_time=1000):
        self.invert = invert
        self.repeat_time = repeat_time
        self.hold_time = hold_time
        self.pin = DigitalInOut(button)
        self.direction = Direction.INPUT
        self.pull = Pull.UP
        self.last_state = False
        self.pressed = False
        self.pressed_time = 0

    def read(self):
        current_time = time.monotonic()
        state = self.raw()
        changed = state != self.last_state
        self.last_state = state

        if changed:
            if state:
                self.pressed_time = current_time
                self.pressed = True
                self.last_time = current_time
                return True
            else:
                self.pressed_time = 0
                self.pressed = False
                self.last_time = 0

        if self.repeat_time == 0:
            return False

        if self.pressed:
            repeat_rate = self.repeat_time
            if self.hold_time > 0 and current_time - self.pressed_time > self.hold_time:
                repeat_rate /= 3
            if current_time - self.last_time > repeat_rate:
                self.last_time = current_time
                return True

        return False

    def raw(self):
        if self.invert:
            return not self.pin.value
        else:
            return self.pin.value

    @property
    def is_pressed(self):
        return self.raw()


class RGBLED:
    def __init__(self, r=board.GP5, g=board.GP6, b=board.GP7, invert=True):
        self.invert = invert
        self.led_r = PWM.PWMOut(r, frequency=1000, duty_cycle=0)
        self.led_g = PWM.PWMOut(g, frequency=1000, duty_cycle=0)
        self.led_b = PWM.PWMOut(b, frequency=1000, duty_cycle=0)

    def set_rgb(self, r, g, b):
        if self.invert:
            r = 255 - r
            g = 255 - g
            b = 255 - b
        self.led_r.duty_cycle(int((r * 65535) / 255))
        self.led_g.duty_cycle(int((g * 65535) / 255))
        self.led_b.duty_cycle(int((b * 65535) / 255))

