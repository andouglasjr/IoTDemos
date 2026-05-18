from micropython import const
import asyncio
import aioble
import bluetooth
import struct
import machine

# Configuração dos Pinos do Joystick na BitDogLab
JOYSTICK_X_PIN = 27 # ADC0
JOYSTICK_Y_PIN = 26 # ADC1
JOYSTICK_BTN_PIN = 22 # Botão (Push button)

adc_x = machine.ADC(JOYSTICK_X_PIN)
adc_y = machine.ADC(JOYSTICK_Y_PIN)
# O botão usa pull-up interno, logo: Pressionado = 0, Solto = 1
btn = machine.Pin(JOYSTICK_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# UUIDs Customizados para o nosso Joystick
# (Gerados aleatoriamente para não conflitar com serviços padrão)
_JOYSTICK_SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
_JOYSTICK_CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")

# Aparência BLE: Gamepad (964)
_ADV_APPEARANCE_GAMEPAD = const(964)
# Frequência do beacon de advertising
_ADV_INTERVAL_MS = 250_000

# Registra o servidor GATT
joy_service = aioble.Service(_JOYSTICK_SERVICE_UUID)
joy_characteristic = aioble.Characteristic(
    joy_service, _JOYSTICK_CHAR_UUID, read=True, notify=True)
aioble.register_services(joy_service)

# Função para empacotar os 3 dados (X, Y, Botão) num único pacote de bytes
def _encode_joystick(x, y, button):
    # Formato do Struct "<HHB":
    # < : Little Endian
    # H : Unsigned Short (2 bytes) -> Para o eixo X (0-65535)
    # H : Unsigned Short (2 bytes) -> Para o eixo Y (0-65535)
    # B : Unsigned Char (1 byte)   -> Para o botão (0 ou 1)
    
    # Invertemos o botão para ficar mais lógico: Pressionado = 1, Solto = 0
    btn_status = 0 if button == 1 else 1
    
    return struct.pack("<HHB", x, y, btn_status)

# Lê o joystick e atualiza a característica BLE
async def sensor_task():
    while True:
        # Leitura dos eixos (retorna valores de 0 a 65535)
        x_val = adc_x.read_u16()
        y_val = adc_y.read_u16()
        btn_val = btn.value()
        
        # Envia os dados empacotados via Bluetooth
        joy_characteristic.write(_encode_joystick(x_val, y_val, btn_val), send_update=True)
        
        # Aguarda 100ms para ter uma leitura fluida do joystick
        await asyncio.sleep_ms(100)

# Espera por conexões. Para de fazer "advertise" enquanto estiver conectado.
async def peripheral_task():
    while True:
        try:
            async with await aioble.advertise(
                _ADV_INTERVAL_MS,
                name="BitDog-Joy",
                services=[_JOYSTICK_SERVICE_UUID],
                appearance=_ADV_APPEARANCE_GAMEPAD,
            ) as connection:
                print("Conexão estabelecida com", connection.device)
                await connection.disconnected()
                print("Dispositivo desconectado")
        except asyncio.CancelledError:
            print("Tarefa periférica cancelada")
        except Exception as e:
            print("Erro na peripheral_task:", e)
        finally:
            await asyncio.sleep_ms(100)

# Roda ambas as tarefas
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)
    
asyncio.run(main())