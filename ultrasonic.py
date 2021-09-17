from machine import Pin
import utime
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print("The distance from object is ",distance,"cm")
while True:
    ultra()
    utime.sleep(1)


'''



from machine import Pin
import utime
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timpassed * 0.0330) / 2
    print('The object can be seen from a distance of',distance, 'cm')

while True:
    ultra()
    utime.sleep(1)









from machine import Pin, Timer
import utime

timer = Timer()
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
led = Pin(16, Pin.OUT)
distance = 0

def get_distance(timer):
    global distance
    trigger.high()
    utime.sleep(0.00001)
    trigger.low()
    
    while echo.value() == 0:
        start = utime.ticks_us()
    while echo.value() == 1:
        stop = utime.ticks_us()
        
    duration = stop - start
    distance = (duration * 0,0343) / 2
    print("Distance:", distance, "cm")
    return distance

timer.init(freq=1, mode=Timer.PERIODIC, callback=get_distance)

while True:
    if distance < 5:
        led.value(1)
    else:
        led.value(0)






import machine
import utime

while True:
  trig=machine.Pin(3, machine.Pin.OUT)
  trig.off() #stop reading
  utime.sleep_us(2)
  trig.on()
  utime.sleep_us(10)
  trig.off()
  echo=machine.Pin(2, machine.Pin.IN)
  while echo.value() == 0:
    pass
  t1 = utime.ticks_us()
  while echo.value() == 1:
    pass
  t2 = utime.ticks_us()
  cm = (t2 - t1) / 58.0
  print(cm)
  utime.sleep(2)

'''