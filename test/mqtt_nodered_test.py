from wifi import Wifi
from micro_mqtt import Micro_MQTT
import time

# --- 1. Creiamo un "Display Finto" ---
# Serve solo per non far rompere la classe Micro_MQTT che si aspetta uno schermo.
class DisplayFinto:
    def fill(self, x): pass
    def text(self, t, x, y): print(f">> LOG DISPLAY: {t}") # Stampiamo su console invece che su schermo
    def show(self): pass
    def clear(self): pass

# --- 2. Configurazioni ---
SSID_WIFI = "A35 di Nick"    # <--- INSERISCI QUI
PASS_WIFI = "Nick0471"    # <--- INSERISCI QUI

# Topic su cui Node-RED deve ascoltare (mqtt in)
TOPIC_INVIO = "pot/air/temperature" 

# --- 3. Connessione Wi-Fi ---
print("--- Inizio connessione Wi-Fi ---")
my_wifi = Wifi()
my_wifi.connect(SSID_WIFI, PASS_WIFI)

# Attendiamo la connessione
while not my_wifi.is_connected():
    print(".", end="")
    time.sleep(0.5)

print("\nWi-Fi Connesso!")

# --- 4. Connessione MQTT ---
# Passiamo il DisplayFinto invece di quello vero
mqtt_device = Micro_MQTT("ESP32_Test_NoDisplay", DisplayFinto())

print("Connessione al Broker MQTT...")
# Ci connettiamo senza sottoscrivere nulla per ora (topic=None)
mqtt_device.connect_and_subscribe(topic=None) 

# --- 5. Loop di Invio a Node-RED ---
conteggio = 0

while True:
    try:
        # Prepariamo il messaggio
        messaggio = f"{conteggio}"
        
        print(f"Sto inviando a Node-RED: {conteggio}")
        
        # Pubblichiamo direttamente usando il client interno
        # Nota: Convertiamo stringhe in bytes se necessario, ma umqtt spesso lo gestisce
        mqtt_device.client.publish(TOPIC_INVIO, messaggio)
        
        conteggio += 1
        
        # Aspetta 5 secondi prima del prossimo invio
        time.sleep(5)
        
    except OSError as e:
        print("Errore di connessione o invio. Riprovo...")
        time.sleep(5)
        # Opzionale: chiamare mqtt_device.restart_and_reconnect() se la connessione cade spesso