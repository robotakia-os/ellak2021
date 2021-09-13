from machine import Pin, ADC
from time import sleep

sensor = ADC(Pin(26))

while True:
    print(sensor.read_u16()) # μη προσημασμένη τιμή 16bit (εύρος: 0-65535)
    sleep(0.5)