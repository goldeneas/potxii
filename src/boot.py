from hcsr04 import HCSR04
from home_screen import HomeScreen
from humidity import Humidity
from pump import Pump
from three_led import ThreeLedPWM
from wifi import Wifi
from micro_mqtt import MicroMQTT
from ssd1306 import SSD1306_I2C
from machine import I2C
from dht import DHT22
from tsl2561 import TSL2561
import time

i2c = I2C(scl=22, sda=21)
display = SSD1306_I2C(128, 64, i2c);
wifi = Wifi(display);
mqtt = MicroMQTT("potxii", display);

wifi.connect("nicola", "nicola-hotspot2")
mqtt.connect("broker.hivemq.com", 1883, None, None)

#topic per dht
mqtt.subscribe("pot/air/temperature")
mqtt.subscribe("pot/air/humidity")

#topic per humidity
mqtt.subscribe("pot/ground/humidity")

#topic per hcsr04 e pompa
mqtt.subscribe("pot/water/water_level")
mqtt.subscribe("pot/water/pump")

#topic per tsl2561
mqtt.subscribe("pot/light/light_level")
mqtt.subscribe("pot/light/led")

#topic per wifi
mqtt.subscribe("pot/system/wifi")

#importiamo i pin 
hcsr04 = HCSR04(17,4)
dht = DHT22(15)
three_led = ThreeLedPWM(32,33,25) 
tsl2561 = TSL2561(i2c)
humidity = Humidity(35)
pump = Pump(26)

def mqtt_handler(topic, msg):
    global pump

    if (not topic == "pot/water/pump"):
        return

    time_s = int(msg)
    # pump.on_for(time_s)
    print("Ho ricevuto secondi: " + str(time_s))

mqtt.set_handler(mqtt_handler)

home_screen = HomeScreen(hcsr04, mqtt, display, wifi, dht, tsl2561, humidity)

while True:
    home_screen.measure()
    home_screen.show()
    time.sleep_ms(200)
