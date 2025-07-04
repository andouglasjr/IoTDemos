import coap.microcoapy as microcoapy
import network

# Conecta  rede Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('BENVENUTO', 'zeliaeluis')
while not wlan.isconnected():
    pass

def receivedMessageCallback(packet, sender):
    print('Message received:', packet.toString(), ', from: ', sender)
    print('Message payload: ', packet.payload.decode('unicode_escape'))

client = microcoapy.Coap()
client.responseCallback = receivedMessageCallback
client.start()

_SERVER_IP="192.168.0.113"
_SERVER_PORT=5683
bytesTransferred = client.get(_SERVER_IP, _SERVER_PORT, "current/measure")
print("[GET] Sent bytes: ", bytesTransferred)

client.poll(2000)

client.stop()