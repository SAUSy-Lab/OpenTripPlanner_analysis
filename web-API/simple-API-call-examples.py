##########################################################################
# simple example GET API calls to a local server running on localhost:8080 
##########################################################################

import requests, json, time

# make a call to the route-planning function
# doc'ed at http://dev.opentripplanner.org/apidoc/1.0.0/resource_PlannerResource.html

# There are more options available. These are just some.
options = {
	'fromPlace':'43.63725,-79.434928',
	'toPlace':'43.646448,-79.3880',
	'time':'1:02pm',
	'date':'11-14-2017',
	'mode':'TRANSIT,WALK',
	'maxWalkDistance':1000,
	'clampInitialWait':0,
	'wheelchair':False
}
response = requests.get(
	"http://localhost:8080/otp/routers/ttc/plan",
	params = options
)
# parse from JSON to python dictionary
response = json.loads(response.text)
# e.g. get the travel time of the first itinerary
print response['plan']['itineraries'][0]['duration']



# isochrone travel area function
# returns a polygon geometry
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
