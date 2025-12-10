from machine import Pin, PWM

class ThreeLedPWM:
    def __init__(self, pin_id1,pin_id2, pin_id3, max_pwm_value=1023):
        
        self._pin1 = Pin(pin_id1, Pin.OUT)
        self._pin2 = Pin(pin_id2, Pin.OUT)
        self._pin3 = Pin(pin_id3, Pin.OUT)
        
        self._max_pwm_value = max_pwm_value
        
        self._pwm1 = PWM(self._pin1)
        self._pwm2 = PWM(self._pin2)
        self._pwm3 = PWM(self._pin3)
        
                  
        self.set_brightness(0)

    def off(self):
        self.set_brightness(0)
        
    def on(self):
        self.set_brightness(100)

    # Valori da 0 100
    def set_brightness(self, value=50):
        duty_cycle = int(value / 100 * self._max_pwm_value)
        
        # Applico il valore a TUTTI e 3 i LED
        self._pwm1.duty(duty_cycle)
        self._pwm2.duty(duty_cycle)
        self._pwm3.duty(duty_cycle)
      