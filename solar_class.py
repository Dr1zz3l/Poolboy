from thermometer_class import thermometer
import time
import datetime
import threading
import pump_lib as pump
import log_lib as log

class solar(threading.Thread):
    def __init__(self, pool = None, thermometer = None, vars = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool = pool
        self.thermometer = thermometer
        self.vars = vars
    
    def run(self):
        while True:
            log.note(datetime.datetime.now().strftime("%Hh %Mm"), "solar")
            log.note("solar wakeup", "solar")
            is_daytime = self.vars.solar_start_time <= datetime.datetime.now().hour < self.vars.solar_stop_time
            if is_daytime and not self.vars.solar_blocked:
                log.note("running main loop", "solar")
                #self.block_pool(True) #forbid pool to circulate
                #log.note("starting short circulation", "solar")
                #pump.solar(True)
                #time.sleep(5) #circulate water to get accurate temperature reading
                #pump.solar(False)
                #time.sleep(15) #wait for thermometers to adjust
                #log.note("finished short circulation", "solar")

                temperatures = self.thermometer.read() #temperature calculations are repeated, could be a function
                avg = (temperatures["solar_schuppen"]+temperatures["solar_sauna"])/2
                log.note("solar temp average: " + str(round(avg,1)) + " C", "solar")
                log.note("pool temp: " + str(round(temperatures["pool"],1)) + " C", "solar")
                if not self.vars.solar_blocked and avg - temperatures["pool"] > self.vars.solar_necessary_temp_delta and temperatures["pool"] < self.vars.solar_max_pool_temp:
                    self.block_pool(True) #block pool pump
                    log.note("replenishing solar", "solar")
                    start_time = time.time()
                    pump.solar(True)
                    while not self.vars.solar_blocked and time.time()-start_time < self.vars.solar_max_circulation_time and avg - temperatures["pool"] > self.vars.solar_cutoff_temp_delta and temperatures["pool"] < self.vars.solar_max_pool_temp:
                        temperatures = self.thermometer.read()
                        avg = (temperatures["solar_schuppen"]+temperatures["solar_sauna"])/2
                        log.note("Solar Sauna: %s, Solar Schuppen: %s, Pool: %s"%(str(round(temperatures["solar_sauna"],1)), str(round(temperatures["solar_schuppen"],1)), str(round(temperatures["pool"],1))), "solar") 
                        time.sleep(self.vars.solar_active_sleep)
                    log.note("replenished solar, interrupted: %s" % str(self.vars.solar_blocked), "solar")
                    pump.solar(False)
                    self.block_pool(False) #allow pool to circulate again
                #wait for next 10min block
                #print("\twaiting for next mutliple of 10min")
                #while datetime.datetime.now().minute % 10 != 0:
                #    print("\tsolar sleep for %s minutes" % str(10-(datetime.datetime.now().minute % 10)))
                #    time.sleep(60)
            else: 
                if not is_daytime: log.note("not daytime", "solar")
                if self.vars.solar_blocked: log.note("blocked", "solar")

            if self.pool.blocked:
                log.note("pool probably blocked from startup", "solar")
                self.block_pool(False)
            log.note("finished main loop", "solar")
            time.sleep(11*60)#wait 11min

    def block_pool(self, value):
        #if self.pool.blocked != value:
        #    time.sleep(2)
        #    self.pool.block(value)
        log.note("blocking pool: "+ str(value), "solar")
        self.pool.block(value)
        time.sleep(5) #wait for water pressure to lower
        

