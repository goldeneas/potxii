# Salva questo file come: main.py
import time
from humidity import Humidity  # Importa la tua classe dal file humidity.py

# --- CONFIGURAZIONE ---
PIN_SENSORE = 34

# Creiamo l'oggetto usando i tuoi parametri di default (4095 e 2500)
# Se vuoi cambiarli, puoi farlo qui: es. Humidity(34, max=4095, min=1500)
sensore = Humidity(PIN_SENSORE, max=4095, min=2500)

print("--- TEST CLASSE HUMIDITY ---")
print("Tieni il sensore all'aria, poi mettilo in acqua.")

try:
    while True:
        # 1. Chiamiamo il metodo .read() per vedere cosa legge l'hardware
        valore_grezzo = sensore.read()
        
        # 2. Chiamiamo il metodo .value() per vedere se la matematica funziona
        percentuale = sensore.value()
        
        # 3. Stampiamo i risultati
        # La 'f' davanti alla stringa serve a inserire le variabili nelle {parentesi}
        print(f"Grezzo: {valore_grezzo}  --->  Percentuale: {percentuale}%")
        
        # Pausa di 1 secondo
        time.sleep(1)

except KeyboardInterrupt:
    print("\nTest terminato.")