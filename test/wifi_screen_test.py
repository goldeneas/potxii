from ssd1306 import SSD1306_I2C
from machine import I2C
from warning_screen import WarningScreen
from wifi_connection_screen import WifiConnectionScreen
import time
from wifi import Wifi

ic = I2C(scl=22, sda=21)
display = SSD1306_I2C(128, 64, ic)

wifi = Wifi()
wifi.connect("PicaNET_5G", "asdasda")

wifi_screen = WifiConnectionScreen(display)
wifi_screen.wait_for_connection("Connecting...", "Connected!", wifi)

time.sleep(3)
