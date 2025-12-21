from machine import Pin, ADC

class Humidity():
    def __init__(self, pin_number, min_val=0, max_val=100):
        # min_val: Valore letto in acqua (massima umidità)
        # max_val: Valore letto in aria (minima umidità)
        pin = Pin(pin_number)
        self.__adc = ADC(pin)
        self.min_val = min_val
        self.max_val = max_val

    def read(self):
        """
        Read a raw value from the LDR.
        :return a value from 0 to 4095.
        """
        return self.__adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return a value from the specified [min, max] range.
        """
        return (self.max_val - self.min_val) * self.read() / 4095

