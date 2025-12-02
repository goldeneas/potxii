import network
import time

from ssd1306 import SSD1306_I2C

class Wifi:
    def __init__(self, ssd1306: SSD1306_I2C):
        self.station = network.WLAN(network.STA_IF)
        self.ssid = ""
        self.display = ssd1306
        self.drawn_low = False
        self.wifi_low = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xe0, 0x0f, 0xf0, 0x18, 0x18, 0x03, 0xc0, 0x07, 0xe0, 0x04, 0x20, 0x01, 0x80, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ])
        self.wifi_high = bytearray([0x00, 0x00, 0x07, 0xe0, 0x1f, 0xf8, 0x3f, 0xfc, 0x70, 0x0e, 0x67, 0xe6, 0x0f, 0xf0, 0x18, 0x18, 0x03, 0xc0, 0x07, 0xe0, 0x04, 0x20, 0x01, 0x80, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    
    def set_active(self, is_active):
        self.station.active(is_active)

    def connect(self, ssid, password):
        # resettiamo l'interfaccia
        self.set_active(False)
        time.sleep_ms(100)
        self.set_active(True)

        self.station.connect(ssid, password)
        self.ssid = ssid

        while not self.is_connected():
            self.display.clear()
            self.toggle_icon()
            self.display.text("Connecting to", 0, 4, 1)
            self.display.text("[" + self.get_ssid() + "]", 0, 14, 1)
            
            self.display.show()
            time.sleep_ms(500)

        self.display.clear()
        self.draw_wifi_high()
        self.display.text("Connected to", 0, 4, 1)
        self.display.text("[" + self.get_ssid() + "]", 0, 14, 1)
        self.display.show()

    def get_ssid(self):
        return self.ssid

    def is_connected(self):
        return self.station.isconnected()

    def toggle_icon(self):
        if self.drawn_low:
            self.display.draw_image(self.wifi_high, 16, 16, 128-16, 0)
        else:
            self.display.draw_image(self.wifi_low, 16, 16, 128-16, 0)
        
        self.drawn_low = not self.drawn_low

    def draw_wifi_high(self):
            self.display.draw_image(self.wifi_high, 16, 16, 128-16, 0)

    def draw_wifi_low(self):
            self.display.draw_image(self.wifi_low, 16, 16, 128-16, 0)
