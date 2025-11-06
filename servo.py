from machine import Pin, PWM

class Servo:
    def __init__(self, pin_id, duty_min=28, duty_max=128):
        self._duty_min = duty_min
        self._duty_max = duty_max

        self._pin = Pin(pin_id, mode = Pin.OUT)
        self._pwm = PWM(self._pin)

    def set_angle(self, angle):
        duty_min = self._duty_min
        duty_max = self._duty_max
        pwm = self._pwm

        pwm.duty(int(duty_min + (angle/180)*(duty_max-duty_min)))
