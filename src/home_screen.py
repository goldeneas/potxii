from hcsr04 import HCSR04
from ssd1306 import SSD1306_I2C
from hcsr04 import HCSR04
from micro_mqtt import MicroMQTT
from wifi import Wifi
from dht import DHT22
from tsl2561 import TSL2561
from humidity import Humidity
import time

# il serbatoio è vuoto 
WATER_TANK_EMPTY_DISTANCE_MM = 130

class HomeScreen:
    def __init__(self, hcsr: HCSR04, mqtt: MicroMQTT, ssd1306: SSD1306_I2C, wifi: Wifi,
                 dht: DHT22, tsl2561: TSL2561, humidity: Humidity):
        self.hcsr = hcsr
        self.mqtt = mqtt
        self.display = ssd1306
        self.wifi = wifi
        self.dht = dht
        self.tsl2561= tsl2561
        self.humidity = humidity

        self.light_value = 0
        self.water_height = 0
        self.wifi_connected = False
        self.air_temperature = 0
        self.air_humidity = 0
        self.terrain_humidity = 0

        self.check_icon = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x0f, 0x00, 0x1f, 0x70, 0x3e, 0x78, 0x7c, 0x7c, 0xf8, 0x1f, 0xf0, 0x0f, 0xe0, 0x07, 0xc0, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00])
        self.warning_icon = bytearray([0x00, 0x80, 0x01, 0xc0, 0x01, 0xc0, 0x03, 0xe0, 0x03, 0x60, 0x07, 0x70, 0x06, 0x30, 0x0e, 0xb8, 0x0c, 0x98, 0x1c, 0x9c, 0x18, 0x8c, 0x38, 0x0e, 0x30, 0x86, 0x7f, 0xff, 0x7f, 0xff, 0x00, 0x00])

    def show(self):
        self.display.clear()

        warning_messages = []

        if (self.water_height < 0):
            self.water_height=0

        if (not self.wifi_connected):
            warning_messages.append("Wifi disconnesso!!")

        if (len(warning_messages) > 0):
            self.show_warnings(warning_messages)
            return

       
        messages1 = [
                "Light: {:.2f} lux".format(self.light_value),
                "Water: {:.2f} mm".format(self.water_height),
                "Air Temp: {:.0f} C".format(self.air_temperature),
                "Air Hum: {:.0f} " .format(self.air_humidity),
                "Dirt Hum: {:.0f} %" .format(self.terrain_humidity)
         ]

        self.text_all(messages1)
        self.display.show()
       
        
        

    def measure(self):
        self.light_value = self.tsl2561.read()
        self.water_height = WATER_TANK_EMPTY_DISTANCE_MM - self.hcsr.distance_mm() 

        if (self.water_height < 0):
            self.water_height = 0

        self.dht.measure()
        self.air_temperature = self.dht.temperature()
        self.air_humidity = self.dht.humidity()
        self.terrain_humidity = self.humidity.value()
        self.wifi_connected = self.wifi.is_connected()
        
        # Topic per DHT (Aria)
        self.mqtt.publish("pot/air/temperature", str(self.air_temperature))
        self.mqtt.publish("pot/air/humidity", str(self.air_humidity))

        # Topic per Umidità Terreno
        self.mqtt.publish("pot/ground/humidity", str(self.terrain_humidity))

        # Topic per HC-SR04 (Livello Acqua)
        # Nota: 'pump' di solito è un comando (subscribe), non un valore da pubblicare
        self.mqtt.publish("pot/water/water_level", str(self.water_height))

        # Topic per TSL2561 (Luce)
        # Nota: 'led' di solito è un comando (subscribe)
        self.mqtt.publish("pot/light/light_level", str(self.light_value))
        

    def show_warnings(self, warning_messages):
        self.display.draw_image(self.warning_icon, 16, 16, 128-16, 0)
        self.text_all(warning_messages)
        self.display.show()

    def text_all(self, messages):
        for i, message in enumerate(messages):
            self.display.text(message, 0, 4 + i * 10)
