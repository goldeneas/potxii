import time
from three_led import ThreeLedPWM  # Importa la classe dal file led_driver.py

# --- CONFIGURAZIONE PIN ---
# Modifica questi valori in base ai tuoi collegamenti
PIN_LED_1 = 32
PIN_LED_2 = 33
PIN_LED_3 = 25

def main():
    print("Inizializzazione controller LED...")
    
    # Creiamo l'oggetto dalla classe importata
    leds = ThreeLedPWM(PIN_LED_1, PIN_LED_2, PIN_LED_3)
    
    print("Avvio test ciclo infinito (Ctrl+C per fermare)")
    
    try:
        while True:
            # 1. Accensione Massima
            print(" -> ON (100%)")
            leds.on()
            time.sleep(1)
            
            # 2. Spegnimento
            print(" -> OFF (0%)")
            leds.off()
            time.sleep(0.5)
            
            # 3. Luminosità Media
            print(" -> MEDIO (50%)")
            leds.set_brightness(50)
            time.sleep(1)
            
            # 4. Effetto Fade (Dissolvenza)
            print(" -> FADE IN/OUT")
            # Salire
            for i in range(0, 101, 5):
                leds.set_brightness(i)
                time.sleep(0.02)
            # Scendere
            for i in range(100, -1, -5):
                leds.set_brightness(i)
                time.sleep(0.02)
                
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nTest interrotto dall'utente.")
        leds.off()

if __name__ == '__main__':
    main()