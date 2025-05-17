import socket
import time
import random

HOST = '192.168.0.113'  # Endereço IP do servidor (localhost)
PORT = 12345  # Porta que o servidor está escutando

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor ouvindo na porta", PORT)
    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)
        try:
            while True:
                # Gera um valor aleatório
                random_value = random.randint(0, 100)
                # Converte o valor aleatório para string e codifica para bytes
                message = str(random_value)+'\n'
                message = message.encode()
                conn.sendall(message)
                # Espera 1 segundo antes de enviar o próximo valor
                time.sleep(1)
        except ConnectionResetError:
            # Caso o cliente se desconecte
            print("Cliente desconectado")
        except Exception as e:
            # Outros possíveis erros
            print(f"Erro: {e}")
