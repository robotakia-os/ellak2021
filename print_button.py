from machine import Pin
from time import sleep

button = Pin(16, Pin.IN, Pin.PULL_DOWN)

while True:
    pressed = button.value()
    print(pressed)
    sleep(0.5)