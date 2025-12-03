from machine import Pin, ADC

class Humidity:
    def __init__(self, pin, max=4095, min=2500):
        #max=4095 il sensore legge umidità 0% (non è inserito nel terreno)
        #min=2500 il sensore legge umidità 100% (è inserito completamente in acqua)
     
        #A0
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB) # Range 0-3.3V
        
      
        self.val_max = max
        self.val_min = min
        

    def read(self):
        #Restituisce solo il numero puro (0-4095)
        return self.adc.read()


    def value(self):
        #Restituisce la percentuale calcolata (0-100%)
        reading = self.read()
                
       
        # Serve per evitare di avere -5% o 105% se la calibrazione non è perfetta
        calculated = reading
        if calculated > self.val_max: calculated = self.val_max
        if calculated < self.val_min: calculated = self.val_min
        
        
        # 2. Matematica (Inversione e conversione in %)
        perc = (self.val_max - calculated) / (self.val_max - self.val_min) * 100
        
        return int(perc)