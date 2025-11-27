from machine import Pin, ADC

class Potentiometer:
    def __init__(self, pin_id):
        self._pin = Pin(pin_id, Pin.IN)
        self._adc = ADC(self._pin)

        self._adc.atten(ADC.ATTN_11DB)  # Misura 0-3.3V

    # This method returns the raw ADC value ranged according to the resolution of the block,
    # e.g., 0-4095 for 12-bit resolution.
    def read(self):
        return self._adc.read()

    # Read ADC and convert to voltage
    # Returns the voltage read
    def value(self):
        return self.read() * (3.3 / 4095)
