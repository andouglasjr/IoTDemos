import asyncio
from bleak import BleakScanner, BleakClient

# UUID da característica que você deseja subscrever (substitua por seu valor real)
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

def notification_handler(sender, data):
    """Callback para tratar notificações da característica."""
    print(f"Notificação recebida do dispositivo {sender}: {data}")

async def connect_and_subscribe(device):
    print(f"Info: {device.name} - {device.address}")
    try:
        async with BleakClient(device.address) as client:
            if await client.is_connected():
                print(f"Conectado ao dispositivo: {device.name} - {device.address}")

                # Subscreve à característica para receber notificações
                await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

                # Mantém a conexão aberta, escutando por notificações
                print(f"Aguardando notificações do dispositivo {device.name}. Pressione Ctrl+C para encerrar.")
                while True:
                    await asyncio.sleep(1)

                # Não se esqueça de parar a notificação antes de finalizar a conexão
                await client.stop_notify(CHARACTERISTIC_UUID)
            else:
                print(f"Falha ao conectar ao dispositivo {device.name} - {device.address}")
    except Exception as e:
        print(f"Erro ao conectar ou subscrever do dispositivo {device.name}: {e}")

async def discover_and_connect():
    print("Descobrindo dispositivos BLE disponíveis...")
    devices = await BleakScanner.discover()

    # Conectar e subscrever a cada dispositivo descoberto
    tasks = [connect_and_subscribe(device) for device in devices]
    await asyncio.gather(*tasks)

# Executa a função principal
asyncio.run(discover_and_connect())
