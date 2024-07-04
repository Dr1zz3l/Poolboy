import RPi.GPIO as GPIO
import log_lib as log
import datetime

acid_pin = 26
chlorine_pin = 19
power_pin = 20  #pin for power
pump_pin = 21 #pin diverts power to pump

solar_state = True
pool_state = False
GPIO.setmode(GPIO.BCM)

for pin in [acid_pin, chlorine_pin, power_pin, pump_pin]:
   GPIO.setup(pin, GPIO.OUT)
GPIO.output(power_pin, False)
GPIO.output(pump_pin, False)
GPIO.output(acid_pin, False)
GPIO.output(chlorine_pin, False)

def pool(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   if state: GPIO.output(pump_pin, pool_state)  #divert power to pool pump if needed
   GPIO.output(power_pin, state)                #power on/off
   log.note("POOL: %s" % pool_on(), "pump")

def pool_on():
   return ((GPIO.input(pump_pin) == pool_state) and (GPIO.input(power_pin) == True))

def solar(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   if state: GPIO.output(pump_pin, solar_state) #divert power to solar pump if needed
   GPIO.output(power_pin, state)                #power on/off
   log.note("SOLAR: %s" % solar_on(), "pump")

def solar_on():
   return ((GPIO.input(pump_pin) == solar_state) and (GPIO.input(power_pin) == True))

def chlorine(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   GPIO.output(chlorine_pin, state)
   log.note("CHLORINE: %s" % chlorine_on(), "pump")

def chlorine_on():
   return GPIO.input(chlorine_pin) == True

def acid(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   GPIO.output(acid_pin, state)
   log.note("ACID: %s" % acid_on(), "pump")

def acid_on():
   return GPIO.input(acid_pin) == True
