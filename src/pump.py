from machine import Pin
from time import sleep

# Il relè va collegato alla 3.3V
# ATTIVA BASSA
class Pump:
    def __init__(self, in_pin):
        self.pin = Pin(in_pin, Pin.OUT)
        self.pin.value(1);
        pass

    def on_for(self, time_s):
        self.pin.value(0)
        sleep(time_s)
        self.pin.value(1)

    def off(self):
        self.pin.value(1)
