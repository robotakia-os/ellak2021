from machine import Pin
from time import sleep

fan = Pin(16, Pin.OUT)

while True:
    fan.on()
    sleep(3)
    fan.off()
    sleep(3)

