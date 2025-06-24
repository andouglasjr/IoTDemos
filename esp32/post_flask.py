# main.py (ESP32 MicroPython client)
import network
import urequests
import time
import dht
import machine

# Wi-Fi credentials
SSID = 'laica_iot'
PASSWORD = '12345678'

# Flask server details
FLASK_SERVER_IP = '192.168.0.102' # e.g., '192.168.1.100'
FLASK_SERVER_PORT = 5000
FLASK_ENDPOINT = '/data'

d = dht.DHT11(machine.Pin(15))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Network config:', wlan.ifconfig())

def send_post_request():
    connect_wifi()
    url = f"http://{FLASK_SERVER_IP}:{FLASK_SERVER_PORT}{FLASK_ENDPOINT}"
    

    temp, humidity = get_temp_humidity()
    data = {"sensor_id": "ESP32_001", "temperature": temp, "humidity": humidity}
    headers = {'Content-Type': 'application/json'}

    try:
        response = urequests.post(url, json=data, headers=headers)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        response.close()
    except Exception as e:
        print("Error sending POST request:", e)

def get_temp_humidity():
    # coletando dados de umidade e temperatura
    d.measure()
    temperatura = d.temperature() # em °C
    umidade= d.humidity() # em % 
    temperatura_str="Temp: "+str(temperatura)
    umidade_str="Umid: "+str(umidade)+" %"
    print(temperatura_str)
    print(umidade_str)
    return temperatura, umidade


if __name__ == '__main__':
    send_post_request()