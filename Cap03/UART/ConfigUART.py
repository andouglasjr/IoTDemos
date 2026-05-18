# Exemplo de configuração da porta UART usando a biblioteca machine do MicroPython.
# Pode-se usar uma das duas configurações abaixo, dependendo dos requisitos do projeto.

import machine

# Configura a primeira porta UART com uma taxa de baud de 9600 bps
uart = machine.UART(0, baudrate=9600)

# Configura a primeira porta UART com uma taxa de baud de 9600 bps, 8 bits de dados, paridade par e 1 bit de parada.
uart = machine.UART(0, baudrate=9600, bits=8, parity=1, stop=1)