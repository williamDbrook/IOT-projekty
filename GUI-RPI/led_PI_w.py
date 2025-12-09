import network
import socket
from machine import Pin
import time

# Nastav WiFi
ssid = "TVOJE_SSID"
password = "TVOJE_HESLO"

led = Pin(15, Pin.OUT)  # Změň pin podle tvého zapojení

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

print("Pico W IP:", wlan.ifconfig()[0])

# Jednoduchý HTTP server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Server běží na http://", wlan.ifconfig()[0])

while True:
    try:
        cl, addr = s.accept()
        request = cl.recv(1024)
        request = str(request)

        if '/led/on' in request:
            led.value(1)
            response = "LED ON"
        elif '/led/off' in request:
            led.value(0)
            response = "LED OFF"
        else:
            response = "Neznámý příkaz"

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
        cl.send(response)
        cl.close()
    except OSError:
        cl.close()