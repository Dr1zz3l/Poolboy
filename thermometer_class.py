import os
import time
import datetime
import threading

######################################################################
#Zeiten in DE Zeit
#
#
######################################################################

def read_sensor_file(sensor_id): 
    location = '/sys/bus/w1/devices/' + sensor_id + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    return celsius

class thermometer(threading.Thread):
    def __init__(self, vars = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vars = vars
        self.temperature_history = {name: [] for name in self.vars.thermometer_ids.keys()} #temporary temperature storage
    
    def run(self):
        while True:
            durations = {name: [] for name in self.vars.thermometer_ids.keys()}
            new_temperatures = durations.copy()

            for name in self.vars.thermometer_ids.keys(): #umständlich geschrieben für präzise Messzeiten
                thermometer_id = self.vars.thermometer_ids[name]
                start_time = time.time()
                temperature = read_sensor_file(thermometer_id)
                duration = time.time()-start_time
                durations[name] = round(duration, 2)
                temperature = round(temperature, 2)
                new_temperatures[name] = temperature
                self.temperature_history[name].append(temperature)
                if len(self.temperature_history[name]) > self.vars.thermometer_max_temp_loggings: self.temperature_history[name].pop(0)
            self.log(new_temperatures, durations)

    def read(self, names = []):
        if len(names) == 0: names = self.vars.thermometer_ids.keys() #wenn kein Name spezifiziert, return alle Temperaturen
        temperature_history = self.temperature_history.copy() #lokale Kopie für minimale Interferenz mit dem run-loop
        temperatures = {name: temperature_history[name][int(len(temperature_history[name])/2)] for name in names} #Median
        return temperatures
        

    def log(self, temperatures, durations):
        save_file = "thermometer_logs/%s.txt" % datetime.datetime.now().strftime("%Y-%m-%d")
        names = self.vars.thermometer_ids.keys()

        if not os.path.exists(save_file): #file muss neu aufgesetzt werden
            headline = ["time"]
            for name in names: 
                headline.append("temperature_"+name)
                headline.append("duration_"+name)
            headline = ", ".join(headline)
            with open(save_file, "w+") as f:
                f.write(headline)
                f.close()
        now = datetime.datetime.now()
        seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() 
        save_text = [int(seconds_since_midnight)]
        for name in names:
            save_text.append(temperatures[name])
            save_text.append(durations[name])
        save_text = ", ".join([str(element) for element in save_text])
        with open(save_file, "a") as f:
            f.write("\n"+save_text)
