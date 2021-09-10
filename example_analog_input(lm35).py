from machine import ADC, Pin
import time

adc = ADC(Pin(26))

while True:
    value = adc.read_u16()
    volt = (3.3/65535) * value # voltage/3.3 = value/65535 -> voltage = (3.3/65535)*value
    temp = volt * 100 # Για τον LM35 ισχύει: temperature/1 = voltage/0,01 -> temperature = voltage*100
    print(temp)
    time.sleep(1)