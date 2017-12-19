import requests
import json
import time


def isojson(xin,yin,t):
    coords = ('%f, %f' % (yin, xin))
    options = {
        'fromPlace': coords,
        'time':'1:02pm',
        'date':'05-20-2016',
        'mode':'WALK',
        'clampInitialWait':0,
        'wheelchair': False,
        'cutoffSec': t,
        'precisionMeters': 10 # how detailed will this be
    }
    response = requests.get(
        "http://localhost:8080/otp/routers/g/isochrone?",
        params = options
    )
    # parse from JSON to python dictionary
    print response.text
    response = json.loads(response.text)


start = time.time()

isojson(-97.11930,49.89281,1800)

print time.time() - start
