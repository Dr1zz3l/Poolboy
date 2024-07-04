import requests
url = "https://www.pooldigital.de/calctools/active_cl.pl"
ploads = {
    "ph": 7.4,
    "clfree": 0.6,
    "cys": 25,
    "dpdfrom": 0.6,
    "dpdto": 4,
    "aclfrom": 0.16,
    "aclto": 4,
    "size": 50,
    "ox": 55,
    "oxindex": 0,
    "resultonly": 1
    }
r = requests.post(url, data = ploads)

