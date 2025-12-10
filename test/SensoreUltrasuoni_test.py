from machine import Pin
from time import sleep
# Se hai salvato la classe in un file separato 'hcsr04.py', togli il commento qui sotto:
from hcsr04 import HCSR04 

# --- CONFIGURAZIONE PIN ---
# Cambia questi numeri in base al tuo cablaggio e alla tua scheda (ESP32, Pico, ecc.)
# Esempio per ESP32: Trig su GPIO 5, Echo su GPIO 18
PIN_TRIGGER = 5 
PIN_ECHO = 18

def main():
    print("Inizializzazione sensore HC-SR04...")
    
    # Istanzia l'oggetto sensore
    # Nota: echo_timeout_us è opzionale, usa il valore di default se non specificato
    sensor = HCSR04(trigger_pin=PIN_TRIGGER, echo_pin=PIN_ECHO)
    
    print("Avvio letture. Premi Ctrl+C per fermare.")
    
    while True:
        try:
            # Lettura della distanza in centimetri
            distanza = sensor.distance_cm()
            
            # Lettura della distanza in millimetri (opzionale)
            # distanza_mm = sensor.distance_mm()
            
            print(f"Distanza: {distanza:.1f} cm")
            
        except OSError as e:
            # Gestisce il caso in cui il sensore non riceva l'eco (fuori portata o errore cablaggio)
            print("Errore sensore:", e)
        except KeyboardInterrupt:
            print("\nTest interrotto dall'utente.")
            break
            
        # Pausa di 1 secondo tra le letture
        # È importante non scendere sotto i 60ms per evitare interferenze tra i ping
        sleep(1)

# Esegui il main
if __name__ == '__main__':
    main()