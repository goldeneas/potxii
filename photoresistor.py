from machine import Pin, ADC

class Photoresistor:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """
        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        # create an object ADC
        self._adc = ADC(Pin(pin))
        self._min_value = min_value
        self._max_value = max_value

    def read(self):
        """
        Read a raw value from the LDR.
        :return a value from 0 to 4095.
        """
        return self._adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return a value from the specified [min, max] range.
        """
        return (self._max_value - self._min_value) * self.read() / 4095
