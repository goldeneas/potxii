from ssd1306 import SSD1306_I2C

class WarningScreen:
    def __init__(self, display: SSD1306_I2C):
        self.display = display


    def show(self):
        self.text_all(self.warning_messages)
