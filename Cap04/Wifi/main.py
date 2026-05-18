import network
import time
print("Conectando no WiFi", end="")

#Criamos uma conexão do tipo WLAN para comunicação com a internet
sta_if = network.WLAN(network.STA_IF)

#Ativamos o módulo WiFi da placa
sta_if.active(True)

#Usamos o 'Wokwi-GUEST' quando queremos que o wokwi conecte com
#a rede em que o computador está conectado. Se quiser conectar com uma rede específica, use o nome da rede e a senha.
sta_if.connect('Wokwi-GUEST', '')

#Tenta realizar a conexão
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
    
#Se conectado mostra
print(" Conectado!")