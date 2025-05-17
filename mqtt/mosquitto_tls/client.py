import paho.mqtt.client as mqtt
import ssl

client = mqtt.Client()

# Configuração de TLS
client.tls_set(ca_certs="ca.crt",
               certfile="client.crt",
               keyfile="client.key",
               tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(False)  # Verifica a validade dos certificados

# Conectar ao broker MQTT
client.connect("localhost", 8883, 60)
client.loop_start()

