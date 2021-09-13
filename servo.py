from machine import Pin, PWM

servo = Pin(16, Pin.OUT)
pwm = PWM(servo)

pwm.freq(50)                            # 50Hz

degrees = 90

# κατασκευή συνάρτησης με δεδομένα: 2,7ms->180μοίρες, 1,6ms->90μοίρες
pulse_width = (0.012 * degrees + 0.54)  # milliseconds
pulse_width = pulse_width * 1000000     # nanoseconds
pulse_width = int(pulse_width)          # μετατροπή float σε int

pwm.duty_ns(pulse_width)