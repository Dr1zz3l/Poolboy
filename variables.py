main_classes_startup_delay = 30 #on startup pump gets turned off. then there's a time.sleep() to get enough temperature readings for a proper median calculation. Then the main classes get started

pool_max_runtime = 30*60 #for how long the pool pump runs per hour-cycle
pool_start_time = 8 # 8 #h in german time
pool_stop_time = 21 # 21 #h in german time
pool_modulo_value = 2 #pool_class is only active when datetime.datetime.now().hour % pool_modulo_value == pool_modulo_result
pool_modulo_result = 0 #value = 2 and result = 1 for uneven hour, result = 0 for even hour. value = 1 and result = 0 for every hour

solar_start_time = 9 #h in german time
solar_stop_time = 22 #h in german time
solar_cutoff_temp_delta = 3 #temperature delta where solar pump is turned off
solar_necessary_temp_delta = 9 #min temp delta for solar pump to turn on (9k was set)
solar_max_pool_temp = 28 #maximum pool temp for solar class to remain active
solar_active_sleep = 10 #when solar pump is on, check for changes every n seconds
solar_blocked = True #so that probe_class can block solar_class. Value changes
solar_max_circulation_time = 10*60 #solar may run for x min per hour max

thermometer_ids = {
    "solar_sauna": "28-0517c3a792ff",
    "solar_schuppen": "28-0517c17ab6ff",
    "pool": "28-0517c3a559ff"
    }
thermometer_max_temp_loggings = 3

probe_measure_start = 540 #measure probe values measurement starts after... sec.
probe_measure_time = 60 #measure probe values for ...sec and then take average
probe_wait_between_pumps = 60 #wait this long between pumping chlorine and acid
probe_ORP_10_min_val = 680 #690 #if ORP under this val, pump chlorine for 10 min
probe_ORP_5_min_val = 730 #710 #if ORP only under this val, pump chlorine for 5 min
