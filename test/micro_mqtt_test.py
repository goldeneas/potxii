from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from wifi import Wifi
from wifi_connection_screen import WifiConnectionScreen
from micro_mqtt import Micro_MQTT
import time

# --- 1. CONFIGURAZIONE HARDWARE ---
PIN_SDA = 21
PIN_SCL = 22

i2c = I2C(0, sda=Pin(PIN_SDA), scl=Pin(PIN_SCL))
oled = SSD1306_I2C(128, 64, i2c)

# --- 2. GESTIONE WI-FI ---
my_wifi = Wifi()
screen = WifiConnectionScreen(oled)

# Parametri di rete (per Wokwi usare questi esatti)
SSID = "Wokwi-GUEST"
PASSWORD = ""

print("Avvio connessione WiFi...")
my_wifi.connect(SSID, PASSWORD)
screen.wait_for_connection("Connessione...", "WiFi Connesso!", my_wifi)

time.sleep(2) # Pausa di 2 secondi per leggere il messaggio

# --- 3. GESTIONE MQTT ---
client_id = "esp32_client_demo"
mqtt = Micro_MQTT(client_id, oled)

TOPIC = "test/messaggio"

# Si connette al broker e si iscrive
mqtt.connect_and_subscribe(TOPIC)

# --- 4. LOOP PRINCIPALE ---
print("Sistema pronto. In attesa di messaggi...")

while True:
    try:
        mqtt.check_msg()
        time.sleep(0.1)
    except OSError:
        # Se cade la connessione MQTT, prova a riconnettere
        print("Errore nel loop, riavvio...")
        mqtt.restart_and_reconnect()