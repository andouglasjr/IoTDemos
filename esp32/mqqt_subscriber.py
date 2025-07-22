import time
import network
import dht
from machine import Pin

from umqtt.simple import MQTTClient

# Configuraes do sensor DHT11
DHT_PIN = 15  # GPIO onde o sensor DHT11 est conectado

# Inicializa o sensor DHT11
sensor = dht.DHT11(Pin(DHT_PIN))

# Configuraes do MQTT
#Endereo do broker MQTT
MQTT_BROKER = "192.168.0.101"
MQTT_PORT = 1883 
MQTT_TOPIC_TEMPERATURE = b"sensor/temp" 
MQTT_TOPIC_HUMIDITY = b"sensor/humidity" 

MQTT_TOPIC_SUB = b"/projeto/#"
CLIENT_ID = "client_id"
USER = "iot"
PASSWORD = "12345678"

# Funcao para lidar com mensagens recebidas
def sub_cb(topic, msg):
    print((topic, msg))

# Conexo com a rede WiFi
def connect_wifi():
  print("Connecting to WiFi", end="")
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect("BENVENUTO", "luisezelia")
  while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.1)
  print(" Connected!")
  print(wlan.ifconfig())    

# Conexao com o broker MQTT
def connect_mqtt():
    print("Connecting to MQTT broker", end="")
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=USER, password=PASSWORD)
    client.connect()
    print(" Connected!")
    return client

def subscribe_topics(client):
    print("Subscribing to topics", end="")
    client.set_callback(sub_cb)
    client.subscribe(MQTT_TOPIC_SUB)
    print(" Subscribed!")

def publish_data(client):
    print("Publishing data", end="")
    sensor.measure()  # Realiza a leitura do sensor DHT11
    temperature = sensor.temperature()  # Obtém a temperatura
    humidity = sensor.humidity()  # Obtém a umidade
    msg_temp = f"temperature, id=100 temp={temperature}".format(temperature)
    msg_humidity = f"humidity, id=100 humidity={humidity}".format(humidity)
    client.publish(MQTT_TOPIC_TEMPERATURE, str(temperature).encode())
    client.publish(MQTT_TOPIC_HUMIDITY, str(humidity).encode())
    print(" Data published!")

def main():
    print("Starting MQTT Subscriber")
    connect_wifi()  # Conecta ao WiFi
    client = connect_mqtt()  # Conecta ao broker MQTT
    #subscribe_topics(client)  # Inscreve-se nos tópicos

    while True:
        publish_data(client)  # Publica os dados do sensor DHT11
        #client.wait_msg()  # Espera por mensagens recebidas
        time.sleep(10)  # Aguarda 10 segundos antes de publicar novamente

