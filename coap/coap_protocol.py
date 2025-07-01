import socket
import struct
import network

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print('Conectado a rede Wi-Fi:', ssid)

def build_coap_packet(payload):
    # Header CoAP simples: versão 1, tipo confirmável (0), token length 0, código POST (0.02), ID arbitrário
    header = b'\x40\x02\x12\x34'
    token = b''
    options = b'\xb3temp'  # Uri-Path: "temp"
    payload_marker = b'\xff'
    return header + token + options + payload_marker + payload.encode()

def send_coap_message(server_ip, port, payload):
    addr = socket.getaddrinfo(server_ip, port)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = build_coap_packet(payload)
    s.sendto(packet, addr)
    resp, _ = s.recvfrom(1024)
    print('Resposta do servidor:', resp)
    s.close()

# Configurações da rede Wi-Fi
SSID = 'laica_iot_ap'
PASSWORD = '12345678' 
connect_to_wifi(SSID, PASSWORD)

# Exemplo de uso
send_coap_message('192.168.137.94', 5683, '25.6')  # IP do seu servidor Docker
