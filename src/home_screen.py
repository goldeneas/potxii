from ssd1306 import SSD1306_I2C

WATER_TANK_EMPTY_DISTANCE = 0

class HomeScreen:
    def __init__(self, hcsr, mqtt, ssd1306, wifi, dht, photoresistor, humidity):
        self.hcsr = hcsr
        self.mqtt = mqtt
        self.display = ssd1306
        self.wifi = wifi
        self.dht = dht
        self.photoresistor = photoresistor
        self.humidity = humidity

        self.check_icon = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x0f, 0x00, 0x1f, 0x70, 0x3e, 0x78, 0x7c, 0x7c, 0xf8, 0x1f, 0xf0, 0x0f, 0xe0, 0x07, 0xc0, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00])

    def show(self):
        light_value = self.photoresistor.value()
        water_height = WATER_TANK_EMPTY_DISTANCE - self.hcsr.distance_cm() 
        wifi_connected = self.wifi.is_connected()
        mqtt_connected = self.mqtt.is_connected()
        
        self.dht.measure()
        air_temperature = self.dht.temperature()
        air_humidity = self.dht.humidity()

        terrain_humidity = self.humidity.value()

        messages = [
                "Light: " + str(light_value) + "%",
                "Water: " + str(water_height) + " mm",
                "Wifi: " + str(wifi_connected),
                "MQTT: " + str(mqtt_connected),
                "Air Temp: " + str(air_temperature) + "C",
                "Air Hum: " + str(air_humidity),
                "Dirt Hum: " + str(terrain_humidity)
        ]

        self.display.clear()
        self.display.draw_image(self.check_icon, 16, 16, 128-16, 0)
        self.text_all(messages)
        self.display.show()

    def text_all(self, messages):
        for i, message in enumerate(messages):
            self.display.text(message, 0, 4 + i * 10)
