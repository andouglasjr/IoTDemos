import bluetooth
from micropython import const
import struct

# Constantes para os eventos de conexo e desconexo
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

# UUIDs para o servio e caracterstica
_SERVICE_UUID = bluetooth.UUID('12345678-1234-5678-1234-56789abcdef0')
_CHAR_UUID = bluetooth.UUID('12345678-1234-5678-1234-56789abcdef1')

# Define o servio e suas caractersticas
_SERVICE = (
    _SERVICE_UUID,
    (
        (_CHAR_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,),
    ),
)

class BLEServer:
    def __init__(self):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._connections = set()
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_SERVICE,))
        self.mac = self._ble.config('mac')
        print("device:"+str(struct.unpack('<h', self.mac[1])[0]))

        # Inicializa a caracterstica com um valor
        self._ble.gatts_write(self._handle, struct.pack('<h', 100))

        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()

    def _advertise(self, interval_us=500000):
        name = 'ESP32_BLE'
        self._ble.gap_advertise(interval_us, adv_data=self._ble.gap_advertise(adv_data=b'\x02\x01\x06' + bytes((len(name) + 1, 0x09)) + bytes(name, 'utf-8')))

    def update_data(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle, data)

# Cria uma instncia do servidor BLE
ble_server = BLEServer()

# Exemplo de atualizao de dados (deve ser integrado ao seu loop de aplicao ou eventos)
# ble_server.update_data(struct.pack('<h', newValue))
