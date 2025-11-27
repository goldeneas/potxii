import network
import time

class Wifi:
    def __init__(self):
        self.station = network.WLAN(network.STA_IF)
        self.ssid = ""
    
    def set_active(self, is_active):
        self.station.active(is_active)

    def connect(self, ssid, password):
        self.set_active(False)
        time.sleep_ms(100)
        self.set_active(True)

        self.station.connect(ssid, password)
        self.ssid = ssid

    def get_ssid(self):
        return self.ssid

    def is_connected(self):
        return self.station.isconnected()
