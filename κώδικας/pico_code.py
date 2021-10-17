from machine import Pin, ADC, PWM
from time import sleep, time, ticks_us, sleep_us

# δημιουργία αντικειμένων και δήλωση αριθμού pin
pir1Pin = Pin(0, Pin.IN, Pin.PULL_DOWN)   # PIR sensor
pir2Pin = Pin(1, Pin.IN, Pin.PULL_DOWN)   # PIR sensor
light1Pin = Pin(2, Pin.OUT)               # 3W LED
light2Pin = Pin(3, Pin.OUT)               # 3W LED
ldrPin = ADC(Pin(28))                     # LDR sensor
flamePin = Pin(4, Pin.IN, Pin.PULL_UP)    # flame sensor
doorServoPin = Pin(5, Pin.OUT)            # servo
foodServoPin = Pin(6, Pin.OUT)            # servo
pi4CatPin = Pin(8, Pin.IN, Pin.PULL_DOWN) # καλώδιο προς το Pi 4
pi4DogPin = Pin(7, Pin.IN, Pin.PULL_DOWN) # καλώδιο προς το Pi 4
triggerPin = Pin(10, Pin.OUT)             # ακροδέκτης trig του ultrasonic sensor
echoPin = Pin(11, Pin.IN)                 # ακροδέκτης echo του ultrasonic sensor
lm35Pin = ADC(Pin(27))                    # LM35 sensor
relayPin = Pin(12, Pin.OUT)               # έλεγχος ανεμιστήρα μέσω relay
micPin = ADC(Pin(26))                     # sound sensor
pi4MusicPin = Pin(9, Pin.OUT)             # καλώδιο προς το Pi 4

# ορισμός αρχικών τιμών σε μεταβλητές
catTimer = 0
dogTimer = 0
catFeedTime = 0
dogFeedTime = 0

def rotateServo(degrees, servo):            # δημιουργία συνάρτησης για την κίνηση των servo
    pwm = PWM(servo)                        # δημιουργία αντικειμένου pwm της κλάσης PWM
    pwm.freq(50)                            # συχνότητα 50Hz, συνεπώς 50 παλμοί/s
    # κατασκευή συνάρτησης με δεδομένα: 2,7ms->180μοίρες, 1,6ms->90μοίρες
    pulse_width = (0.012 * degrees + 0.54)  # πλάτος παλμού σε milliseconds
    pulse_width = pulse_width * 1000000     # πλάτος παλμού σε nanoseconds
    pulse_width = int(pulse_width)          # μετατροπή float σε int
    return pwm.duty_ns(pulse_width)         # επιστροφή τιμής στο κυρίως πρόγραμμα

def ultrasonic():                           # δημιουργία συνάρτησης για τη μέτρηση απόστασης
    global distance                         # η μεταβλητή distance είναι διαθέσιμη παντού
    timepassed = 0                          # ορισμός αρχικής τιμής
    signalon = 0                            # ορισμός αρχικής τιμής
    signaloff = 0                           # ορισμός αρχικής τιμής
    
    triggerPin.low()                        # δεν αποστέλεται υπέρηχος
    sleep_us(2)                             # διάρκεια σιγής 2μs
    triggerPin.high()                       # αποστολή υπέρηχου 
    sleep_us(5)                             # διάρκεια σήματος 5μs
    triggerPin.low()
    while echoPin.value() == 0:             # μη ανίχνευση ανακλώμενου υπέρηχου
        signaloff = ticks_us()
    while echoPin.value() == 1:             # ανίχνευση ανακλώμενου υπέρηχου
        signalon = ticks_us()
    timepassed = signalon - signaloff       # υπολογισμος χρονικής διάρκειας
    #s=v*t όπου v η ταχύτητα του υπέρηχου, και /2 γιατί ο υπέρηχος διανύει 2 φορές την απόσταση
    distance = (timepassed * 0.0343) / 2
    return distance                         # επιστροφή τιμής (σε cm) στο κυρίως πρόγραμμα

while True:
    ldr = ldrPin.read_u16()      # αναλογική ανάγνωση σήματος αισθητήρα φωτός
    sleep(0.01)                  # μικρή καθυστέρηση για να μετραπεί το σήμα σε ψηφιακό από τον ADC
    pir1 = pir1Pin.value()       # ψηφιακή ανάγνωση του ενός PIR
    pir2 = pir2Pin.value()       # ψηφιακή ανάγνωση του άλλου PIR
    # ενεργοποίηση φωτισμού στο πρώτο δωμάτιο αν δώσει σήμα ο PIR και ο φωτισμός είναι χαμηλός
    if pir1 == 1 and ldr < 15000:
        light1Pin.on()
    else:
        light1Pin.off()
    # ενεργοποίηση φωτισμού στο δεύτερο δωμάτιο αν δώσει σήμα ο PIR και ο φωτισμός είναι χαμηλός
    if pir2 == 1 and ldr < 15000:
        light2Pin.on()
    else:
        light2Pin.off()

    flame = flamePin.value()           # ψηφιακή ανάγνωση του flame sensor
    # περιστροφή servo 140 μοίρες και άνοιγμα πόρτας διαφυγής σε περιπτωση πυρκαγιάς
    if flame == 0:
        rotateServo(140, doorServoPin)
    else:
        rotateServo(0, doorServoPin)

    ultrasonic()             # κλήση της συνάρτησης που επιστρέφει την καταγεγραμμένη απόσταση 
    cat = pi4CatPin.value()  # το Raspberry Pi 4 θα στείλει 1 αν εντοπιστεί γάτα, διαφορετικά 0
    dog = pi4DogPin.value()  # το Raspberry Pi 4 θα στείλει 1 αν εντοπιστεί σκύλος, διαφορετικά 0

    currentTime = time()     # βοηθητική μεταβλητή για να υπολογιστεί αργότερα ο χρόνος που κύλησε
    # γάτα και σκύλος θα φάνε αν εντοπιστούν, πλησιάσουν κοντά και περάσουν 10s από την τελευταία φορά
    if cat == 1 and catTimer > 10 and distance < 20:
        rotateServo(135, foodServoPin) # περιστροφή μηχανισμού δεξιόστροφα για το φαγητό της γάτας
        sleep(0.5)                     # διάρκεια πτώσης τροφής
        rotateServo(90, foodServoPin)  # επιστροφή μηχανισμού στην αρχική θέση
        catFeedTime = time()           # καταγραφή χρονικής στιγμής που έφαγε η γάτα
        cat = 0                        # θα ξαναγίνει 1 όταν ξαναδεί τη γάτα η κάμερα
    elif dog == 1 and dogTimer > 10 and distance < 20:
        rotateServo(45, foodServoPin)  # περιστροφή μηχανισμού αριστερόστροφα για το φαγητό του σκύλου
        sleep(0.5)                     # διάρκεια πτώσης τροφής
        rotateServo(90, foodServoPin)  # επιστροφή μηχανισμού στην αρχική θέση
        dogFeedTime = time()           # καταγραφή χρονικής στιγμής που έφαγε ο σκύλος
        dog = 0                        # θα ξαναγίνει 1 όταν ξαναδεί τον σκύλο η κάμερα
    else:
        rotateServo(90, foodServoPin)  # ο μηχανισμός δεν επιτρέπει σε καμία τροφή να πέσει
    
    catTimer = currentTime - catFeedTime # υπολογισμός χρόνου απ' όταν έφαγε για τη γάτα
    dogTimer = currentTime - dogFeedTime # υπολογισμός χρόνου απ' όταν έφαγε για ο σκύλος
    
    temp = 0                         # βοηθητική μεταβλητή για την εξαγωγή του μέσου όρου 10 μετρήσεων
    for i in range(10):              # εξαγωγή μέσου όρου για να προκύψουν σταθερότερες τιμές
        lm35 = lm35Pin.read_u16()    # αναλογική ανάγνωση σήματος αισθητήρα θερμοκρασίας
        sleep(0.01)                  # μικρή καθυστέρηση για να μετραπεί το σήμα σε ψηφιακό από τον ADC
        # voltage/3.3 = lm35/65535 -> voltage = (3.3/65535)*lm35
        voltage = (3.3/65535) * lm35 # μετατροπή τιμής σήματος σε τιμή τάσης
        # Για τον LM35 ισχύει: temperature/1 = voltage/0,01 -> temperature = voltage*100
        temperature = voltage * 100  # μετατροπή τιμής τάσης σε τιμή θερμοκρασίας σε βαθμούς Κελσίου
        temp = temp + temperature    # η καινούρια μέτρηση προστίθεται στην παλιά
    temp = temp / 10                 # διαίρεση με το 10 για να προκύψει ο μέσος όρος 
    # ενεργοποίηση ανεμιστήρα μέσω του relay αν η θερμοκρασία είναι υψηλή
    if temp > 32:
        relayPin.on()
    else:
        relayPin.off()
    
    micValue = micPin.read_u16()     # αναλογική ανάγνωση σήματος αισθητήρα ήχου
    sleep(0.01)                      # μικρή καθυστέρηση για να μετραπεί το σήμα σε ψηφιακό από τον ADC
    # αποστολή 1 ή 0 προς το Raspberry Pi 4 αν η ένταση του ήχου ξεπεράσει κάποιο κατώφλι
    if micValue > 20000:
        pi4MusicPin.on()
        sleep(0.5)
    else:
        pi4MusicPin.off()
    # εμφάνιση τιμών θερμοκρασίας στην οθόνη του υπολογιστή (αν επιλέξουμε να τον συνδέσουμε στο Pico)
    print(temp) 

