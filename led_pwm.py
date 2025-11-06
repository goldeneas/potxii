from machine import Pin, PWM

class LedPWM:
    def __init__(self, pin_id, max_pwm_value=1023):
        self._pin = Pin(pin_id, Pin.OUT)
        self._max_pwm_value = max_pwm_value
        self._pwm = PWM(self._pin)

    # value between 0 and 100
    def set_brightness(self, value=50):
        self._pwm.duty(value / 100 * self._max_pwm_value)
