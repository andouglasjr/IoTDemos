#importando as classes ADC e Pin da biblioteca machine
from machine import ADC
from machine import Pin

#importando a biblioteca time
import time

#inicializando uma variável chamada adc0 que usa a classe ADC e o id_da_porta que será usada.
adc0=ADC(0)

#inicia o laço de repetição infinito
while True:
    print(adc0.read_u16()) #exibe no terminal a leitura do adc0
    time.sleep_ms(500) #dorme por 500 ms