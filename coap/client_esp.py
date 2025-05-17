from microcoapy.microcoapy import Coap
import network
import time

# Conecta à rede Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('your-ssid', 'your-password')
while not wlan.isconnected():
    pass

# Configura o cliente CoAP
coap = Coap()
coap.start()

# Define o IP do servidor CoAP e a porta
server_ip = '192.168.1.100'
server_port = 5683

# Envia um pacote CoAP POST para o servidor
uri_path = 'sensor/data'
payload = 'temperature=24.5&humidity=60'
coap.post(server_ip, server_port, uri_path, payload, None, Coap.CONTENT_FORMAT.COAP_TEXT_PLAIN)

# Aguarda um pouco antes de fechar
time.sleep(2)

coap.stop()
