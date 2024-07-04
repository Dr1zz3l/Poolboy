import RPi.GPIO as GPIO
import time

pin = int(input("Welcher Pin soll angesteuert werden? (Cl: 19 / Ph: 26) "))
dt = float(input("Für wieviele Sekunden soll Pin %s an sein? " %pin))

GPIO.setmode(GPIO.BCM)  
GPIO.setup(pin, GPIO.OUT) 

t0 = time.time()

while time.time() < t0 + dt:
    if GPIO.input(pin) == False:
        GPIO.output(pin, not True) #Relay on
    time.sleep(.1)
    
GPIO.output(pin, not False) #Relay off