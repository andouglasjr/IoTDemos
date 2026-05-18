# Utilizando o display OLED com I2C no ESP32
# Este exemplo mostra como configurar e usar um display OLED com interface I2C no ESP32 usando a biblioteca ssd1306. O display é inicializado, limpo e uma mensagem "IoT" é exibida.

from machine import Pin, I2C
import ssd1306
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("IoT", 0, 2)
oled.show()