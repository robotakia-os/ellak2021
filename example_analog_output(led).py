from machine import Pin, PWM
from time import sleep

led = PWM(Pin(21))

led.freq(1000)

while True:
    for i in range(0, 65025, 1):
        led.duty_u16(i)
        sleep(0.0001)
    for i in range(65025, 0, -1):
        led.duty_u16(i)
        sleep(0.0001)