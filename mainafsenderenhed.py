import network
import espnow
from machine import UART
import time,sys , uselect

uart_port = 2
uart_speed = 9600

station = network.WLAN(network.STA_IF)
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)

uart = UART(uart_port, uart_speed)
usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)

print("Ready to receive!")
while True:
    host, msg = esp_now.recv()
    try:
        if host == b'\xb0\xa72\xdeK\x0c':
            ToBytes = msg.decode('Ascii')
            print("Received from")
            print(host)
            print("Message containing")
            print(ToBytes)
            if msg and host == b'\xb0\xa72\xdeK\x0c':           
                uart.write(ToBytes)
                print("Sending!")
                if ToBytes == '\n':
                    break
    except AttributeError:
        pass
