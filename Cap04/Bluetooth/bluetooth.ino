// Esse exemplo mostra como usar o Bluetooth Serial no ESP32. Ele permite que você envie dados do monitor serial para um dispositivo Bluetooth emparelhado e vice-versa. Certifique-se de que o Bluetooth esteja habilitado no seu ambiente de desenvolvimento e que o dispositivo esteja emparelhado com o ESP32.

// Inclusão da biblioteca
#include "BluetoothSerial.h"
// O "if" a seguir verifica se o o Bluetooth está habilitado
#if !defined(CONFIG_BT_ENABLED) ||
!defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// Cria uma instância da biblioteca
BluetoothSerial SerialBT;
void setup()
{
    // Inicializa a Serial
    Serial.begin(115200);
    // Inicializa o Bluetooth com o nome ESP32Test
    SerialBT.begin("ESP32test");
    Serial.println("Dispositivo iniciado! Pode realizar o pareamento...");
}
void loop()
{
    if (Serial.available())
    {
        // Se disponível na serial, escreve no Bluetooth
        SerialBT.write(Serial.read());
    }
    // Se disponível na Bluetooth, escreve na Serial
    if (SerialBT.available())
    {
        Serial.write(SerialBT.read());
    }
    delay(20);
}