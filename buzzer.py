from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self, pin_id):
        self.pwm = PWM(Pin(pin_id, Pin.OUT))
        self.pwm.duty(0)  # Inizialmente spento

    # max duty is 1023
    def play(self, melodies, wait, duty):
        for note in melodies:
            if note == 0:
                self.pwm.duty(0) # Pausa
            else:
                self.pwm.freq(note)
                self.pwm.duty(duty)
            time.sleep_ms(wait) # Durata della nota
        self.stop() # Ferma il suono alla fine

    def stop(self):
        self.pwm.duty(0)  # Spegne il suono
