import asyncio
import struct
from bleak import BleakClient

def notification_handler(sender, data):
    print(f"Recebido de {sender}: {struct.unpack('<h', data)[0]}")

async def main(ble_address, char_uuid):
    async with BleakClient(ble_address) as client:
        # Verifique se a conexão foi estabelecida
        if await client.is_connected():
            print(f"Conectado ao dispositivo {ble_address}")

            # Ative as notificações da característica
            await client.start_notify(char_uuid, notification_handler)

            # Aguarde para continuar recebendo dados. Ajuste conforme necessário
            await asyncio.sleep(30)

            # Desative as notificações ao concluir
            await client.stop_notify(char_uuid)
        else:
            print("Não foi possível conectar ao dispositivo.")

# Substitua pelos valores do seu dispositivo
ble_address = "24:6F:28:17:CA:92"
char_uuid = "12345678-1234-5678-1234-56789abcdef1"

# Executar o loop principal
asyncio.run(main(ble_address, char_uuid))
