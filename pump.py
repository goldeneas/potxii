from machine import Pin
from time import sleep_ms

class Pump:
    def __init__(self, in_pin):
        self.pin = Pin(in_pin, Pin.OUT)
        self.pin.value(1);
        pass

    def on_for(self, time_ms):
        self.pin.value(0)
        sleep_ms(time_ms)
        self.pin.value(1)

    def off(self):
        self.pin.value(1)
