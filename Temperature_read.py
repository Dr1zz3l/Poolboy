import time

zeit_anf = time.time()

thermometers = {"solar sauna": "28-0517c3a792ff",
                "solar schuppen": "28-0517c17ab6ff",
                "pool": "28-0517c3a559ff"}

def read(sensor):
    location = '/sys/bus/w1/devices/' + sensor + '/w1_slave'
    zeit = time.time() - zeit_anf
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    delta = time.time() - zeit - zeit_anf
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    return [zeit, delta, celsius]

def log():
    x = 1
    while x:
        with open("zeit_pool.txt","a") as f:
            out_p = read("28-0517c3a559ff")
            f.write("%s, %s, %s\n" % (str(out_p[0]), str(out_p[1]), str(out_p[2]) ))
            f.close()
        
        with open("zeit_sauna.txt","a") as f:
            out_s = read("28-0517c3a792ff")
            f.write("%s, %s, %s\n" % (str(out_s[0]), str(out_s[1]), str(out_s[2]) ))
            f.close()
        
        with open("zeit_schuppen.txt","a") as f:
            out_u = read("28-0517c17ab6ff")
            f.write("%s, %s, %s\n" % (str(out_u[0]), str(out_u[1]), str(out_u[2]) ))
            f.close()
       
        with open("temperatures.txt","w") as f:
            f.write("%s, %s, %s" % (str(out_p[2]), str(out_s[2]), str(out_u[2]) ))
            f.close()
       
        with open("temperatures.txt","r") as f:
            print(f.read())
            f.close()
                        
       
log()
