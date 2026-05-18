# Rode este código em um ambiente de desenvolvimento para ESP32 com suporte a SPI, como o Wokwi, Arduino IDE ou PlatformIO. Ele utiliza a biblioteca Adafruit_ILI9341 para controlar um display TFT ILI9341 conectado via SPI. O código inicializa o display, define a rotação, cor e tamanho do texto, e exibe a mensagem "Hello IoT". Certifique-se de conectar os pinos TFT_DC e TFT_CS corretamente ao seu ESP32.
# Exemplo 3.2 da apostila

#include <Adafruit_ILI9341.h>

#define TFT_DC 2
#define TFT_CS 15
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

void setup() {
    tft.begin();
    tft.setRotation(1);
    tft.setTextColor(ILI9341_WHITE);
    tft.setTextSize(2);
    tft.print("Hello IoT");
}
void loop() {}