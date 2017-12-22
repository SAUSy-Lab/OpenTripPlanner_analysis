# generates geojsons of fastest route from origin to destinations by different modes using OpenTripPlanner
# from inputs of many origins in a csv file and array of university campuses for destinations

import requests
import polyline
import csv
import json
import time
import ast

# function for converting list of coordinates into open big list
def coord_list_convert(coord_list):
    out_geo = []
    for xy in coord_list:
        lat = xy[0]
        lon = xy[1]
        out_geo.append([lon,lat])
    return out_geo

start_time = time.time()

campus = [
['Scarborough (UTSC)',-79.18749,43.78521],
['Downtown Toronto (St. George)',-79.396949,43.663219],
['Mississauga (UTM)',-79.663787,43.548233],
['Keele',-79.503068,43.77317],
['Glendon',-79.379745,43.727538],
['RyersonU',-79.378994,43.657951],
['OCADu',-79.391032,43.652692]
]

# string for url for biking
bike_tri = '&optimize=TRIANGLE&triangleTimeFactor=0&triangleSlopeFactor=0&triangleSafetyFactor=1'

fail_list = []

# input data
with open("data.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    t = 0
    w = 0
    b = 0
    i = 0
    # loop over
    for row in reader:

        # grab coordinates for each row
        o_lat = row['Y']
        o_lon = row['X']

        # destination from campus array - which school are you going to?
        for camp in campus:
            if row['pscampusmain'] == camp[0]:
                d_lon = float(camp[1])
                d_lat = float(camp[2])

        # get get url for specific modes
        if row['psmainmodefalltypicalaggr'] == 'Local Transit' or row['psmainmodefalltypicalaggr'] == 'Regional Transit':
            mode = 'TRANSIT, WALK'
            url_string = "http://localhost:8080/otp/routers/default/plan?fromPlace=" + str(o_lat) + "%2C" + str(o_lon) + "&toPlace=" + str(d_lat) + "%2C" + str(d_lon) + "&time=8:00am&date=07-20-2016&mode=WALK,TRANSIT&maxWalkDistance=5000&arriveBy=false&wheelchair=false&locale=en"
            t += 1
        elif row['psmainmodefalltypicalaggr'] == 'Walk':
            mode = 'WALK'
            url_string = "http://localhost:8080/otp/routers/default/plan?fromPlace=" + str(o_lat) + "%2C" + str(o_lon) + "&toPlace=" + str(d_lat) + "%2C" + str(d_lon) + "&time=8:00am&date=07-20-2016&mode=WALK&maxWalkDistance=999999&arriveBy=false&wheelchair=false&locale=en"
            w += 1
        elif row['psmainmodefalltypicalaggr'] == 'Bike':
            mode = 'BICYCLE'
            url_string = "http://localhost:8080/otp/routers/default/plan?fromPlace=" + str(o_lat) + "%2C" + str(o_lon) + "&toPlace=" + str(d_lat) + "%2C" + str(d_lon) + "&time=8:00am&date=07-20-2016&mode=BICYCLE&maxWalkDistance=5000&arriveBy=false&wheelchair=false&locale=en" + bike_tri
            b += 1

        else:
            mode = 'NONE'

        if mode != 'NONE':
            print mode
            print url_string
            try:

                # request data
                page = requests.get(url_string)

                line_coords = []

                # convert result into dictionary
                dic = json.loads(page.content)

                # number of legs in journey
                leg_len = len(dic['plan']['itineraries'][0]['legs'])

                # grab coordinates for each leg
                l = 0
                while l < leg_len:
                    # grabs and decodes points along each segment leg
                    pts = dic['plan']['itineraries'][0]['legs'][l]['legGeometry']['points']
                    line_geom = polyline.decode(pts)
                    line_coords = line_coords + line_geom
                    l += 1

                # convert all legs into one linestring
                coordinates = coord_list_convert(line_coords)

                # grab info that may be usefule
                duration = dic['plan']['itineraries'][0]['duration']
                walk_dist = dic['plan']['itineraries'][0]['walkDistance']
                walk_time = dic['plan']['itineraries'][0]['walkTime']
                transit_time = dic['plan']['itineraries'][0]['transitTime']
                wait_time = dic['plan']['itineraries'][0]['waitingTime']
                transfers = dic['plan']['itineraries'][0]['transfers']

                # set up geojson schema and code in coordinates and whatever properties
                geojson = {
                    "type": "FeatureCollection","features": [
                    {
                      "type": "Feature",
                      "properties": {
                        "duration": duration,
                        "ID": row['rowID']
                      },
                      "geometry": {
                        "type": "LineString",
                        "coordinates": coordinates
                      }
                    }
                  ]
                }

                # write geojsons
                file_name = str(row['rowID']) + '.geojson'
                with open("otp_geojsons/" + file_name, 'w') as fp:
                    json.dump(geojson, fp)

                # print how long all that took for single iteration
                print "+" * 10
                i += 1
                print i
                print time.time() - start_time

            # add to a list any that fail
            except:
                fail_list.append(row['rowID'])
                print 'fail'

# print result counts and any ids that failed
print "+" * 10
print t, w, b, t + w + b
print time.time() - start_time
print fail_list
print len(fail_list)

