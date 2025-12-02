from pump import Pump
import time

# --- CONFIGURAZIONE ---
# Inserisci qui il numero del GPIO collegato al relè/pompa
PIN_POMPA = 14  

def run_test():
    print("--- Inizio Test Pompa ---")
    
    # 1. Test Inizializzazione
    # La pompa dovrebbe rimanere SPENTA (Pin HIGH)
    print(f"Inizializzazione su GPIO {PIN_POMPA}...")
    try:
        my_pump = Pump(PIN_POMPA)
        print(">> OK: Oggetto creato. Verifica che la pompa sia SPENTA.")
    except OSError as e:
        print(f">> ERRORE: Impossibile inizializzare il pin. {e}")
        return

    time.sleep(2) # Pausa per verifica visiva

    # 2. Test attivazione temporizzata (on_for)
    # La pompa deve ACCENDERSI (Pin LOW) per 3 secondi, poi SPEGNERSI
    DURATA = 5000
    print(f"Attivazione pompa per {DURATA/1000} secondi...")
    my_pump.on_for(DURATA)
    print(">> OK: Ciclo finito. Verifica che la pompa si sia SPENTA.")

    time.sleep(2)

    # 3. Test spegnimento manuale (off)
    # Serve a garantire che il metodo off() riporti il pin a HIGH
    print("Test comando manuale off()...")
    my_pump.off()
    print(">> OK: Comando inviato.")

    print("--- Test Completato ---")

if __name__ == "__main__":
    run_test()