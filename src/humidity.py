from machine import Pin
from machine import ADC

class Humidity():
    def __init__(self, pin_number):
        pin = Pin(pin_number)
        self.__adc = ADC(pin)
        self.__adc.atten(ADC.ATTN_11DB)

    def read(self):
        adc_reading = self.__adc.read()
        return adc_reading

    def value(self, adc_max = 4095):
        adc_reading = self.read()
        return (100 * adc_reading) / adc_max
