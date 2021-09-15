from machine import Pin
from time import sleep
import _thread

internal_led = Pin(25, machine.Pin.OUT)
pir = Pin(15, Pin.IN, Pin.PULL_DOWN)
internal_led.off()
def second_thread():
    while True:
        if pir.value() == 1:
            internal_led.on()
            sleep(5)
            internal_led.off()

_thread.start_new_thread(second_thread, ())

while True:
    print("Hello, I'm here writting every second")
    sleep(1)