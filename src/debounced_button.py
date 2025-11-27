from machine import Pin
import time

REQUIRED_ACTIVE_TICKS = 4
BOUNCING_MAX_DELTA_MS = 200

class DebouncedButton():
    def __init__(self, id, pull):
        self._pin = Pin(id, Pin.IN, pull)
        self._last_pressed_timestamp = 0

    def set_irq(self, callback, trigger):
        self._callback = callback
        self._pin.irq(lambda btn: self._on_press(btn), trigger)

    def _on_press(self, btn):
        now = time.ticks_ms()

        diff = time.ticks_diff(now, self._last_pressed_timestamp)
        if (diff < BOUNCING_MAX_DELTA_MS):
            return

        active_ticks = 0
        while btn.value() and active_ticks < REQUIRED_ACTIVE_TICKS:
            time.sleep_ms(5)
            active_ticks += 1

        if (active_ticks < REQUIRED_ACTIVE_TICKS):
            return

        self._last_pressed_timestamp = now
        self._callback(btn)
