from micropython import const
import uasyncio as asyncio
import aioble
import bluetooth
import struct
import machine

# Configuração do LED onboard (ajuste o pino se a sua placa receptora não for uma Pico W padrão)
try:
    led = machine.Pin("LED", machine.Pin.OUT)
    led.on()
except:
    pass # Ignora caso a placa não tenha o pino "LED" mapeado assim

# UUIDs Customizados idênticos aos definidos no transmissor (BitDogLab)
_JOYSTICK_SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
_JOYSTICK_CHAR_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")

# Nome do periférico que queremos conectar (já configurado por você)
peripheral_name = "BitDog-Joy"

# Função para desempacotar os dados recebidos (2 inteiros de 16 bits + 1 byte)
def _decode_joystick(data):
    try:
        if data is not None:
            # Desempacota o formato "<HHB" (X, Y, Botão)
            return struct.unpack("<HHB", data)
    except Exception as e:
        print("Erro ao decodificar joystick:", e)
    return None

async def find_joystick():
    # Escaneia por 5 segundos
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            if result.name():
                print("Encontrado:", result.name())
            # Verifica se o nome e o serviço batem com o nosso Joystick
            if result.name() == peripheral_name and _JOYSTICK_SERVICE_UUID in result.services():
                return result.device
    return None

async def main():
    while True:
        device = await find_joystick()
        if not device:
            print("Joystick não encontrado. Tentando novamente em 5s...")
            await asyncio.sleep_ms(5000)
            continue

        try:
            print("Conectando a", device)
            connection = await device.connect()
        except asyncio.TimeoutError:
            print("Timeout durante a conexão. Tentando novamente...")
            await asyncio.sleep_ms(5000)
            continue

        async with connection:
            try:
                # Descobre o serviço e a característica customizados
                joy_service = await connection.service(_JOYSTICK_SERVICE_UUID)
                joy_characteristic = await joy_service.characteristic(_JOYSTICK_CHAR_UUID)
                
                # INSCRIÇÃO NAS NOTIFICAÇÕES: Recebe dados assim que são enviados
                await joy_characteristic.subscribe()
            except asyncio.TimeoutError:
                print("Timeout ao descobrir serviços. Tentando novamente...")
                await asyncio.sleep_ms(5000)
                continue
            except Exception as e:
                print("Erro ao configurar serviços:", e)
                break

            print("Conectado! Aguardando dados do Joystick...")
            while True:
                try:
                    # Fica aguardando a notificação chegar (sem precisar de sleep)
                    joy_data = await joy_characteristic.notified()
                    
                    if joy_data is not None:
                        decoded_data = _decode_joystick(joy_data)
                        if decoded_data is not None:
                            x, y, btn = decoded_data
                            status_botao = "Pressionado" if btn == 1 else "Solto"
                            # Formato limpo: X,Y,B (Ex: 32768,32768,0)
                            print(f"{x},{y},{btn}")
                            # Imprime os dados formatados (05d garante que o número tenha sempre 5 dígitos)
                            # print(f"Eixo X: {x:05d} | Eixo Y: {y:05d} | Botão: {status_botao}")
                        else:
                            print("Dados inválidos recebidos.")
                except Exception as e:
                    print("Conexão perdida ou erro no loop:", e)
                    break  # Sai do loop interno e tenta reconectar

# Cria o Event Loop
loop = asyncio.get_event_loop()
# Cria a tarefa para rodar a função principal
loop.create_task(main())

try:
    # Roda o loop infinitamente
    loop.run_forever()
except Exception as e:
    print('Ocorreu um erro: ', e)
except KeyboardInterrupt:
    print('Programa interrompido pelo usuário')