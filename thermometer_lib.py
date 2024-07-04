import datetime

thermometers = {"solar sauna": "28-0517c3a792ff",
                "solar schuppen": "28-0517c17ab6ff",
                "pool": "28-0517c3a559ff"}

def read(sensor):
    location = '/sys/bus/w1/devices/' + sensor + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    return celsius


def log(temperatures):
    datetime_string = datetime.datetime.utcnow().strftime("%d-%b-%Y (%H:%M:%S)")
    with open("temperature_log.txt", "a") as f:
        f.write(datetime_string +"\n")
        for key in temperatures.keys():
            f.write("%s: %s\n" % (key, str(temperatures[key])))
        f.write("\n\n")
        f.close()
    
if __name__ == "__main__":
    for key in thermometers.keys():
        print(key, read(thermometers[key]))
