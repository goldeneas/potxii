from ssd1306 import SSD1306_I2C
from wifi import Wifi
import time

class WifiConnectionScreen:
    def __init__(self, display: SSD1306_I2C):
        self.display = display
        self.drawn_low = False
        self.wifi_low = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xe0, 0x0f, 0xf0, 0x18, 0x18, 0x03, 0xc0, 0x07, 0xe0, 0x04, 0x20, 0x01, 0x80, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ])
        self.wifi_high = bytearray([0x00, 0x00, 0x07, 0xe0, 0x1f, 0xf8, 0x3f, 0xfc, 0x70, 0x0e, 0x67, 0xe6, 0x0f, 0xf0, 0x18, 0x18, 0x03, 0xc0, 0x07, 0xe0, 0x04, 0x20, 0x01, 0x80, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    
    def wait_for_connection(self, message: str, connected_message: str, wifi: Wifi):
        while not wifi.is_connected():
            self.display.clear()
            self.toggle_icon()
            self.display.text(message, 0, 4, 1)
            self.display.text("[" + wifi.get_ssid() + "]", 0, 14, 1)
            
            self.display.show()
            time.sleep_ms(500)

        self.display.clear()
        self.draw_wifi_high()
        self.display.text(connected_message, 0, 4, 1)
        self.display.text("[" + wifi.get_ssid() + "]", 0, 14, 1)
        self.display.show()
            
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
