#importamos a classe Pin da biblioteca machine
from machine import Pin

#Usa a classe Pin para definir um pino chamado "led"
#Pin(id_da_porta, modo)
# modo: IN (porta de entrada) - Receber dados
# modo: OUT (porta de saída) - Envida dados
led = Pin(5, Pin.OUT)

#Atribui o valor 1 (HIGH) para o pino
led.value(1)