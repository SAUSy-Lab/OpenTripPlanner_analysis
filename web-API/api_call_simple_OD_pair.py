
import requests, json, time

# make a call to the route-planning function
# doc'ed at http://dev.opentripplanner.org/apidoc/1.0.0/resource_PlannerResource.html

# There are more options available. These are just some.
options = {
	'fromPlace':'43.807030915856686,-79.45655822753905',
	'toPlace':'43.83180253191123,-79.30652618408203',
	'time':'4:20pm',
	'date':'10-16-2019',
	'mode':'TRANSIT,WALK',
	'maxWalkDistance':10000,
	'clampInitialWait':0,
	'numItineraries': 10,

	 # 'bannedAgencies': "GO", # remove if including GO transit (commuter transit)
	'wheelchair':False
}

# send to server and get data
response = requests.get(
	"http://localhost:8080/otp/routers/default/plan",
	params = options
)

# parse from JSON to get a dictionary of the first shown itinerary
trip_info = (json.loads(response.text))["plan"]["itineraries"]

print((trip_info))

# print the url as well if needed
print(response.url)
