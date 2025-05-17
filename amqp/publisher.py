import pika

# Conecta ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Envia uma mensagem para a fila
channel.basic_publish(exchange='topic',
        routing_key='ker.error',
                      body='Only testing!')

print(" [x] Sent 'Only testing!'")
connection.close()
