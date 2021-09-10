from machine import Pin
import time

ledred = Pin(21, Pin.OUT)               #output
ledgreen = Pin(20, Pin.OUT)             #output
button = Pin(19, Pin.IN, Pin.PULL_DOWN) #input

while True:
    if button.value() == 1:
        ledred.off()
        for i in range (3):
            ledgreen.on()         #or led.value(1)
            time.sleep(0.5)
            ledgreen.off()        #or led.value(0)
            time.sleep(0.5)
    else:
        ledgreen.off()
        ledred.on()