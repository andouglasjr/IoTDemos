from microcoapy import Coap
import network
import time

# Conecta à rede Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('laica_iot_ap', '12345678')
while not wlan.isconnected():
    pass

# Configura o cliente CoAP
coap = Coap()
coap.start()

# Define o IP do servidor CoAP e a porta
server_ip = '192.168.137.94'
server_port = 5683

def send_data(payload):
    # Envia um pacote CoAP GET para o servidor
    uri_path = 'sensor/data'
    coap.post(server_ip, server_port, uri_path, bytearray(payload, 'utf-8'), None, 0)

payload = 'temperature=24.5&humidity=60'
send_data(payload)


# Aguarda um pouco antes de fechar
time.sleep(2)
def close_coap():
    coap.stop()
