import time
import network
from umqtt.simple import MQTTClient

# Configuraes do MQTT
#Endereo do broker MQTT
MQTT_BROKER = "192.168.0.102"
#Porta do broker MQTT padro 
MQTT_PORT = 1883 
#Tpico MQTT
MQTT_TOPIC = b"area/1/sensor/1/temperatura'" 

# Identificao do cliente MQTT
CLIENT_ID = "client_id"

USER = "iot"
PASSWORD = "12345678"

# Funcao para lidar com mensagens recebidas
def sub_cb(topic, msg):
    print((topic, msg))

print("Connecting to WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("laica_iot", "12345678")
while not wlan.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")
print(wlan.ifconfig())    

# Conexo com o broker MQTT
client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=USER, password=PASSWORD)
client.set_callback(sub_cb)
client.connect()

# Publicao de uma mensagem no tpico MQTT
client.publish(MQTT_TOPIC, b"Hello, MQTT!")

# Espera por mensagens recebidas
client.wait_msg()

# Desconecta do broker MQTT
client.disconnect()