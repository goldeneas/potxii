import network
import time

class Wifi:
    def __init__(self):
        self.station = network.WLAN(network.STA_IF)
    
    def set_active(self, is_active):
        self.station.active(is_active)

    def connect(self, ssid, password):
        self.station.active(True)
        self.station.connect(ssid, password)

    def is_connected(self):
        return self.station.is_connected()
