from machine import Pin, ADC

class Humidity():
    def __init__(self, pin_number, min_val=1500, max_val=4095):
        # min_val: Valore letto in acqua (massima umidità)
        # max_val: Valore letto in aria (minima umidità)
        pin = Pin(pin_number)
        self.__adc = ADC(pin)
        self.__adc.atten(ADC.ATTN_11DB) # Range 0-3.3V (circa)
        self.min_val = min_val
        self.max_val = max_val

    def read(self):
        return self.__adc.read()

    def value(self):
        adc_reading = self.read()
        
        # Mappa il valore letto tra 0% e 100% usando i limiti reali
        # La logica è inversa: lettura alta = secco, lettura bassa = bagnato
        if adc_reading >= self.max_val:
            return 0
        elif adc_reading <= self.min_val:
            return 100
        else:
            # Formula di mappatura lineare inversa
            return (self.max_val - adc_reading) / (self.max_val - self.min_val) * 100
