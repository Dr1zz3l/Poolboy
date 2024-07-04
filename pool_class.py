import time
import threading
import datetime
import pump_lib as pump
import thermometer_lib as thermometer
import log_lib as loggen
from thermometer_lib import thermometers

class pool(threading.Thread):
    def __init__(self, vars = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vars = vars

        self.pump_on = False #False = off, True = on
        self.blocked = True #at program start, the solar class will instantly block. no need to start pump for a few milliseconds
        self.current_hour = (datetime.datetime.now().hour-1)%24 #so that it always starts with a new hour
        self.runtime = 0 #seconds
        self.ran_since = 0 #seconds (time.time())

    def run(self):
        msg = ""
        while True:
            blocked = self.blocked
            is_daytime = self.vars.pool_start_time <= datetime.datetime.now().hour < self.vars.pool_stop_time
            good_hour_modulo = datetime.datetime.now().hour%self.vars.pool_modulo_value == self.vars.pool_modulo_result
            new_msg = "blocked: %s, is_daytime: %s, good_hour_modulo: %s" % (str(blocked), str(is_daytime), str(good_hour_modulo))
            if new_msg != msg:
                msg = new_msg
                loggen.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "pool", 2)
                loggen.note(msg, "pool")
            if not blocked and is_daytime and good_hour_modulo:
                if datetime.datetime.now().hour != self.current_hour: #if new hour, reset values
                    loggen.note("new hour, reset values", "pool")
                    if self.pump_on: #print for how long pool pump was on in last hour
                        loggen.note("absolute runtime this hour: " + str(self.runtime + time.time()-self.ran_since), "pool")
                    else:
                        loggen.note("absolute runtime this hour: " + str(self.runtime), "pool")
                    loggen.note("new hour, reset values", "pool")
                    self.current_hour = datetime.datetime.now().hour
                    self.runtime = 0
                    self.ran_since = time.time() #allows for pump to stay on when hour changes

                if self.runtime < self.vars.pool_max_runtime and not self.pump_on: #if pump should be turned on
                    loggen.note("pool pump needs to be turned on", "pool")
                    self.pump_state(True)
                
                if self.pump_on and self.runtime + (time.time()-self.ran_since) >= self.vars.pool_max_runtime: #ran for long enough
                    loggen.note("pool pump reached max runtime", "pool")
                    self.pump_state(False)
            else: 
                if self.pump_on: 
                    loggen.note("turning off because blocked or too early/late or wrong hour modulo", "pool")
                    self.pump_state(False)
            time.sleep(1)

    def block(self, state):
        self.blocked = state
        if self.blocked and self.pump_on:
            self.pump_state(False)
        loggen.note("\n\t\tpool blocked: "+ str(state))
        
    def pump_state(self, state):
        self.pump_on = state 
        if self.pump_on: #set values for runtime calculation
            self.ran_since = time.time()
        else: 
            self.runtime += time.time()-self.ran_since
            loggen.note("\n\t\talready ran for " + str(round(self.runtime)) + " seconds")
        pump.pool(state)
            
