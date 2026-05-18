import machine
import time
import Cap03.SPI.Micropython.ssd1306 as ssd1306

# SPI pins - ajuste conforme sua placa
spi = machine.SPI(1, baudrate=10000000, polarity=0, phase=0,
                  sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))

dc = machine.Pin(16, machine.Pin.OUT)
res = machine.Pin(17, machine.Pin.OUT)
cs = machine.Pin(5, machine.Pin.OUT)

oled = ssd1306.SSD1306_SPI(128, 64, spi, dc, res, cs)
led = machine.Pin(2, machine.Pin.OUT)


def update_display(state):
    oled.fill(0)
    oled.text('SPI SSD1306', 0, 0)
    oled.text('LED {}'.format('ON' if state else 'OFF'), 0, 16)
    oled.show()
    led.value(1 if state else 0)


while True:
    update_display(True)
    time.sleep(1)
    update_display(False)
    time.sleep(1)
