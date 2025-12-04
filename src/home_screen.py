from hcsr04 import HCSR04
from ssd1306 import SSD1306_I2C
from hcsr04 import HCSR04
from micro_mqtt import MicroMQTT
from wifi import Wifi
from machine import DHT22
from photoresistor import Photoresistor
from humidity import Humidity

# TODO: dobbiamo trovare la lettura del sensore ad ultrasuoni
# quando il serbatoio è vuoto ed inserirla qui
WATER_TANK_EMPTY_DISTANCE = 11.3

class HomeScreen:
    def __init__(self, hcsr: HCSR04, mqtt: MicroMQTT, ssd1306: SSD1306_I2C, wifi: Wifi,
                 dht: DHT22, photoresistor: Photoresistor, humidity: Humidity):
        self.hcsr = hcsr
        self.mqtt = mqtt
        self.display = ssd1306
        self.wifi = wifi
        self.dht = dht
        self.photoresistor = photoresistor
        self.humidity = humidity

        self.light_value = 0
        self.water_height = 0
        self.wifi_connected = False
        self.mqtt_connected = False
        self.air_temperature = 0
        self.air_humidity = 0
        self.terrain_humidity = 0

        self.check_icon = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x0f, 0x00, 0x1f, 0x70, 0x3e, 0x78, 0x7c, 0x7c, 0xf8, 0x1f, 0xf0, 0x0f, 0xe0, 0x07, 0xc0, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00])
        self.warning_icon = bytearray([0x00, 0x80, 0x01, 0xc0, 0x01, 0xc0, 0x03, 0xe0, 0x03, 0x60, 0x07, 0x70, 0x06, 0x30, 0x0e, 0xb8, 0x0c, 0x98, 0x1c, 0x9c, 0x18, 0x8c, 0x38, 0x0e, 0x30, 0x86, 0x7f, 0xff, 0x7f, 0xff, 0x00, 0x00])

    def show(self):
        self.display.clear()

        warning_messages = []

        light_value = self.photoresistor.value()
        water_height = WATER_TANK_EMPTY_DISTANCE - self.hcsr.distance_cm() 
        if (water_height < 0):
            warning_messages.append("Ricalibrare sensore acqua")

        wifi_connected = self.wifi.is_connected()
        if (not wifi_connected):
            warning_messages.append("Wifi disconnesso!!")

        mqtt_connected = self.mqtt.is_connected()
        if (not mqtt_connected):
            warning_messages.append("MQTT disconnesso!!")
        
        self.dht.measure()
        air_temperature = self.dht.temperature()
        air_humidity = self.dht.humidity()

        terrain_humidity = self.humidity.value()

        if (len(warning_messages) > 0):
            self.show_warnings(warning_messages)
            return

        messages = [
                "Light: " + str(light_value) + "%",
                "Water: " + str(water_height) + " mm",
                "Wifi: " + str(wifi_connected),
                "MQTT: " + str(mqtt_connected),
                "Air Temp: " + str(air_temperature) + "C",
                "Air Hum: " + str(air_humidity),
                "Dirt Hum: " + str(terrain_humidity)
        ]

        self.display.draw_image(self.check_icon, 16, 16, 128-16, 0)
        self.text_all(messages)
        self.display.show()

    def measure():
        self.light_value = self.photoresistor.value()
        self.water_height = WATER_TANK_EMPTY_DISTANCE - self.hcsr.distance_cm() 
        self.wifi_connected = self.wifi.is_connected()
        self.mqtt_connected = self.mqtt.is_connected()

        self.dht.measure()
        self.air_temperature = self.dht.temperature()
        self.air_humidity = self.dht.humidity()
        self.terrain_humidity = self.humidity.value()

    def show_warnings(self, warning_messages):
        self.display.draw_image(self.warning_icon, 16, 16, 128-16, 0)
        self.text_all(warning_messages)
        self.display.show()

    def text_all(self, messages):
        for i, message in enumerate(messages):
            self.display.text(message, 0, 4 + i * 10)
