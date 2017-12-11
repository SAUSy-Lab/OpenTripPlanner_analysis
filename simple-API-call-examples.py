##########################################################################
# simple example GET API calls to a local server running on localhost:8080 
##########################################################################

import requests, json

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

# MORE TO COME...
