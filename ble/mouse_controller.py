import serial
import pyautogui
import time

# ================= CONFIGURAÇÕES =================
PORTA_SERIAL = 'COM5'  # Mude para a sua porta serial (ex: 'COM5', '/dev/ttyUSB0')
BAUD_RATE = 115200

# O ADC da placa vai de 0 a 65535. O centro físico do joystick fica em torno de 32768.
CENTRO = 32768
ZONA_MORTA = 4000      # Ignora pequenas variações para o mouse não tremer sozinho
SENSIBILIDADE = 1500   # Quanto menor o número, mais rápido o mouse se move

# Segurança do PyAutoGUI: Se o mouse enlouquecer, jogue-o para um dos cantos da tela para parar o script
pyautogui.FAILSAFE = True 
pyautogui.PAUSE = 0    # Remove o delay padrão do PyAutoGUI para movimentos fluidos
# =================================================

try:
    print(f"Conectando na porta {PORTA_SERIAL}...")
    ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=0.1)
    print("Conectado! Lendo dados do joystick...")
except Exception as e:
    print(f"Erro ao abrir a porta serial: {e}")
    exit()

estado_anterior_botao = 0

while True:
    try:
        # Lê a linha da serial e limpa espaços e quebras de linha
        linha = ser.readline().decode('utf-8').strip()
        
        if linha:
            # Esperamos o formato "X,Y,Botao" (Ex: 32768,32768,1)
            partes = linha.split(',')
            
            if len(partes) == 3:
                x_raw = int(partes[0])
                y_raw = int(partes[1])
                botao = int(partes[2])
                
                # --- Lógica de Movimento ---
                dx = 0
                dy = 0
                
                # Eixo X (Pode precisar inverter o sinal '-' dependendo de como a placa está montada)
                if x_raw > (CENTRO + ZONA_MORTA):
                    dx = (x_raw - CENTRO) / SENSIBILIDADE
                elif x_raw < (CENTRO - ZONA_MORTA):
                    dx = (x_raw - CENTRO) / SENSIBILIDADE
                    
                # Eixo Y (Geralmente o Y do PC é invertido em relação ao joystick)
                if y_raw > (CENTRO + ZONA_MORTA):
                    dy = (y_raw - CENTRO) / SENSIBILIDADE
                elif y_raw < (CENTRO - ZONA_MORTA):
                    dy = (y_raw - CENTRO) / SENSIBILIDADE
                
                # Move o mouse se houver variação fora da zona morta
                if dx != 0 or dy != 0:
                    # O Y é invertido fisicamente: subir o joystick move pra cima (Y negativo no PC)
                    pyautogui.move(int(dx), int(-dy))
                
                # --- Lógica do Clique ---
                # Detecta a transição de "solto" (0) para "pressionado" (1)
                if botao == 1 and estado_anterior_botao == 0:
                    pyautogui.mouseDown()
                # Detecta a transição de "pressionado" (1) para "solto" (0)
                elif botao == 0 and estado_anterior_botao == 1:
                    pyautogui.mouseUp()
                
                estado_anterior_botao = botao

    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
        break
    except ValueError:
        # Ignora linhas mal formatadas/lixo na serial
        pass
    except Exception as e:
        print(f"Erro inesperado: {e}")
        break

ser.close()