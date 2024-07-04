import threading
import datetime
import time
import Atlas_I2C
import pump_lib as pump
import log_lib as log
    
class probes(threading.Thread):
    def __init__(self, vars = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.vars = vars
        self.ORP = False
        self.pH = False

        devices = Atlas_I2C.get_devices()
        module_ORP = "ORP"
        module_pH = "pH"

        for d in devices:
            log.note("found d._module %s" % d._module, "probe")
            if d._module == module_ORP: self.ORP = d
            elif d._module == module_pH: self.pH = d
        if not self.ORP: log.note("Device %s not found" % module_ORP, "probe")
        if not self.pH: log.note("Device %s not found" % module_pH, "probe")

        self.current_hour = (datetime.datetime.now().hour-1)%24 #so that it always starts with a new hour. for testing purposes
            
    def run(self):
        self.vars.solar_blocked = False
        log.note("unblocked solar", "probe")
        while True:
            now = datetime.datetime.now()
            new_hour = now.hour != self.current_hour
            is_daytime = self.vars.pool_start_time <= now.hour < self.vars.pool_stop_time
            good_hour_modulo = now.hour%self.vars.pool_modulo_value == self.vars.pool_modulo_result
            not_first_cycle = (now.hour - self.vars.pool_start_time) >= self.vars.pool_modulo_value

            if new_hour and is_daytime and good_hour_modulo and not_first_cycle:
                log.note(now.strftime("%Hh %Mm %Ss"), "probe", 2)
                log.note("start hourly cycle", "probe")
                self.current_hour = now.hour
                self.block_solar(True)
                time.sleep(10) #give pool_class time to turn on pump

                if not pump.pool_on(): #abort cycle if pool_pump is off
                    log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "probe")
                    log.note("pool pump didn't turn on, abort this cycle 1", "probe")
                    continue #jump to beginning of loop

                log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "probe")
                time.sleep(self.vars.probe_measure_start) #wait until measurment starts to settle values
                log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "probe")
                
                t_0 = time.time() #timer
                ORP_values = []
                pH_values = []
                while time.time() < t_0 + self.vars.probe_measure_time: #take measurements for x seconds
                    self.ORP.write("R")
                    self.pH.write("R")
                    time.sleep(min([self.ORP.long_timeout, self.pH.long_timeout]))
                    data = self.ORP.read().replace("\x00","").split(" ")
                    if data[0] == "Success":
                        ORP_values.append(float(data[-1]))
                    data = self.pH.read().replace("\x00","").split(" ")
                    if data[0] == "Success":
                        pH_values.append(float(data[-1]))
                
                ORP_val = sum(ORP_values)/len(ORP_values) #take averages
                pH_val = sum(pH_values)/len(pH_values)
                
                log.note(datetime.datetime.now().strftime("%Hh %Mm %Ss"), "probe")
                log.note("ORP: "+str(ORP_val), "probe")
                log.note("pH: "+str(pH_val), "probe")

                ORP_t = self.ORP_correction_time(ORP_val) #get pump times
                pH_t = self.pH_correction_time(pH_val)

                if not pump.pool_on(): #abort cycle if pool_pump is off
                    log.note("pool pump didn't turn on, abort this cycle 2", "probe")
                    continue #jump to beginning of loop

                if ORP_t > 0: self.pump_chlorine(ORP_t)

                time.sleep(self.vars.probe_wait_between_pumps)
                if not pump.pool_on(): #abort cycle if pool_pump is off
                    log.note("pool pump didn't turn on, abort this cycle 3", "probe")
                    continue #jump to beginning of loop

                if pH_t > 0: self.pump_acid(pH_t)

                self.block_solar(False)

                

    def block_solar(self, value):
        self.vars.solar_blocked = value
        if value: time.sleep(self.vars.solar_active_sleep) #give solar_class time to block itself

    def get_ORP(self):
        self.ORP.write("R")
        time.sleep(self.ORP.long_timeout)
        return self.ORP.read()

    def get_pH(self):
        self.pH.write("R")
        time.sleep(self.pH.long_timeout)
        return self.pH.read()

    def ORP_correction_time(self, val): #determine how long the pump needs to run
        if val < self.vars.probe_ORP_10_min_val:
            return 10*60
        elif val < self.vars.probe_ORP_5_min_val:
            return 5*60
        else:
            return 0
    
    def pH_correction_time(self, val): #determine how long the pump needs to run
        if val > self.vars.probe_pH_10_min_val:
            return 10*60
        elif val > self.vars.probe_pH_5_min_val:
            return 5*60
        else:
            return 0

    def pump_chlorine(self, dt): #pump on/off
        log.note("pumping chlorine for %ss"%str(dt), "probe")
        t0 = time.time()
        while time.time() < t0 + dt and pump.pool_on():
            if not pump.chlorine_on(): pump.chlorine(True)
            time.sleep(.01)
        pump.chlorine(False)

    def pump_acid(self, dt): #pump on/off
        log.note("pumping acid for %ss"%str(dt), "probe")
        t0 = time.time()
        while time.time() < t0 + dt and pump.pool_on():
            if not pump.acid_on(): pump.acid(True)
            time.sleep(.01)
        pump.acid(False)
