import time
import network
import ahtx0 as ahtx0
from ssd1306 import SSD1306_I2C
import json
from machine import Pin, I2C, SoftI2C

from umqtt.simple import MQTTClient

# Configuraes do sensor DHT11
DHT_PIN = 15  # GPIO onde o sensor DHT11 est conectado

# Inicializa o i2c
i2c0 = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)  # Inicializa o display OLED
oled.fill(0)  # Limpa o display OLED


sensor = ahtx0.AHT10(i2c0) # Inicializa o sensor AHT10

# Configuraes do MQTT
#Endereo do broker MQTT
MQTT_BROKER = "192.168.0.101"
MQTT_PORT = 1883 
MQTT_TOPIC_TEMPERATURE = b"/sensor/bitdoglab/" 
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
    oled.text("Connecting to WiFi", 0, 0)
    oled.show()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("laica_iot", "12345678")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")
    oled.text("Connected!", 0, 10)
    oled.show()
    print(wlan.ifconfig())    

# Conexao com o broker MQTT
def connect_mqtt():
    print("Connecting to MQTT broker", end="")
    oled.text("Connecting to MQTT", 0, 20)
    oled.show()
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=USER, password=PASSWORD)
        client.connect()
        print(" Connected!")
        oled.text("Connected!", 0, 30)
        oled.show()
    except Exception as e:
        print("Failed to connect to MQTT broker:", e)
        oled.text("Failed to connect MQTT", 0, 30)
        oled.show()
        return None
    return client

def subscribe_topics(client):
    print("Subscribing to topics", end="")
    client.set_callback(sub_cb)
    client.subscribe(MQTT_TOPIC_SUB)
    print(" Subscribed!")

def publish_data(client):
    try:
        print("Publishing data", end="")
        temp = sensor.temperature  # Obtém a temperatura
        humidity = sensor.relative_humidity  # Obtém a umidade

        payload = json.dumps({
            "temperature": temp,
            "humidity": humidity
        })
    
        #msg_temp = f"temperature, id=100 temp={temperature}".format(temperature)
        #msg_humidity = f"humidity, id=100 humidity={humidity}".format(humidity)
        client.publish(MQTT_TOPIC_TEMPERATURE, payload.encode())
        #client.publish(MQTT_TOPIC_HUMIDITY, str(sensor.relative_humidity).encode())
        print(" Data published!")
        oled.fill(0)  # Limpa o display OLED
        oled.text("Temp: {:.2f} C".format(temp), 0, 0)
        oled.text("Humidity: {:.2f} %".format(humidity), 0, 10)
        oled.show()  # Atualiza o display OLED
    except Exception as e:
        print("Failed to publish data:", e)
        oled.text("Failed to publish", 0, 20)
        oled.show()  


print("Starting MQTT Subscriber")
connect_wifi()  # Conecta ao WiFi
client = connect_mqtt()  # Conecta ao broker MQTT
#subscribe_topics(client)  # Inscreve-se nos tópicos

while True:
    publish_data(client)  # Publica os dados do sensor DHT11
    #client.wait_msg()  # Espera por mensagens recebidas
    time.sleep(10)  # Aguarda 10 segundos antes de publicar novamente

