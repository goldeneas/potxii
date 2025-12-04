from hcsr04 import HCSR04
from home_screen import HomeScreen
from humidity import Humidity
from photoresistor import Photoresistor
from wifi import Wifi
from micro_mqtt import MicroMQTT
from ssd1306 import SSD1306_I2C
from machine import I2C
from dht import DHT22
import time

i2c = I2C(scl=22, sda=21)
display = SSD1306_I2C(128, 64, i2c);
wifi = Wifi(display);
mqtt = MicroMQTT(display);

# aspetta che la connessione sia stabilita
# TODO: e se non ci connettiamo?
wifi.connect("TESTSSID", "TESTPASSWORD")

# TODO: deve aspettare che siamo connessi
# TODO: e se non ci connettiamo?
mqtt.connect("potxii", "test.mosquitto.org", 1883)

hcsr04 = HCSR04(-1, -1)
dht = DHT22(-1)
photoresistor = Photoresistor(-1)
humidity = Humidity(-1)

home_screen = HomeScreen(hcsr04, mqtt, display, wifi, dht, photoresistor, humidity)

while True:
    home_screen.measure()
    home_screen.show()
    time.sleep_ms(200)
