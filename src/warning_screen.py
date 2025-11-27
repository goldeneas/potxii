from ssd1306 import SSD1306_I2C

class WarningScreen:
    def __init__(self, display: SSD1306_I2C):
        self.display = display
        self.messages = []
        self.warning_icon = bytearray([0x00, 0x80, 0x01, 0xc0, 0x01, 0xc0, 0x03, 0xe0, 0x03, 0x60, 0x07, 0x70, 0x06, 0x30, 0x0e, 0xb8, 0x0c, 0x98, 0x1c, 0x9c, 0x18, 0x8c, 0x38, 0x0e, 0x30, 0x86, 0x7f, 0xff, 0x7f, 0xff, 0x00, 0x00])

    def append_message(self, message: str):
        message_idx = len(self.messages)
        self.messages.append(message)
        return message_idx
    
    def remove_message(self, message_idx):
        self.messages.pop(message_idx)

    def show(self):
        self.display.draw_image(self.warning_icon, 16, 16, 128-16, 0)
        
        for idx, message in enumerate(self.messages):
            self.display.text("- " + message, 0, idx * 10, 1)
        
        self.display.show()
