import RPi.GPIO as GPIO
import log_lib as log
import datetime

acid_pin = 26
chlorine_pin = 19
power_pin = 20  #pin for power
pump_pin = 21

solar_state = True
pool_state = False
GPIO.setmode(GPIO.BCM)  
for pin in [acid_pin, chlorine_pin, power_pin, pump_pin]:
   GPIO.setup(pin, GPIO.OUT)    
GPIO.output(power_pin, False)
GPIO.output(pump_pin, False)

def pool(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   if state: GPIO.output(pump_pin, not pool_state)  #divert power to pool pump if needed
   GPIO.output(power_pin, not state)                #power on/off
   log.note("POOL: %s" % pool_on(), "pump")

def pool_on():
   return ((GPIO.input(pump_pin) != pool_state) and (GPIO.input(power_pin) == False))

def solar(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   if state: GPIO.output(pump_pin, not solar_state) #divert power to splar pump if needed
   GPIO.output(power_pin, not state)                #power on/off
   log.note("SOLAR: %s" % solar_on(), "pump")

def solar_on():
   return ((GPIO.input(pump_pin) != solar_state) and (GPIO.input(power_pin) == False))

def chlorine(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   GPIO.output(chlorine_pin, not state)
   log.note("CHLORINE: %s" % chlorine_on(), "pump")

def chlorine_on():
   return GPIO.input(chlorine_pin) == False

def acid(state):
   log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pump")
   GPIO.output(acid_pin, not state)
   log.note("ACID: %s" % acid_on(), "pump")

def acid_on():
   return GPIO.input(acid_pin) == False
