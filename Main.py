from thermometer_class import thermometer
import time
import variables
import solar_class
import pool_class
import thermometer_class
import probe_class
import pump_lib as pump
import log_lib as loggen

loggen.note("%"*60)
loggen.note("solar class output", "solar")
loggen.note("pool class output", "pool")
loggen.note("probe output", "probe")
loggen.note("pump output", "pump")
loggen.note("%"*60)
loggen.note(n = 3)

pump.pool(False)
thermometer = thermometer_class.thermometer(variables)
thermometer.start()
time.sleep(variables.main_classes_startup_delay)
pool = pool_class.pool(variables)
pool.start()
solar = solar_class.solar(pool, thermometer, variables)
solar.start()
probes = probe_class.probes(variables)
probes.start()
