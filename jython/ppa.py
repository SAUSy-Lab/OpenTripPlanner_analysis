# computes time potential path area (PPA) between two points
# for whatever travel time specifications are required
# outputs results are tied to a network graph

# inputs required
# 2 points, # gtfs and osm to build graph, # location of graph nodes

# make sure graph is connected before running!
# (e.g. no islands, etc.)

# this works well for modes that aren't time dependent (e.g. walking, biking)
# not precise for transit (e.g. varying schedules) as it it 
# routes start and mid point on the same departure time
# so there is room from improvement!

# run via ...
# jython -Dpython.path=otp.jar ppa.py



from org.opentripplanner.scripting.api import *
import time
import csv

# time script
start_time = time.time()

# input points
point_A = [43.726620, -79.482133]
point_B = [43.652990, -79.398005]
max_travel_time = 3600


in_data = [point_A,point_B]

# initial load graph - have graphs store in "graphs" folder and routing set up
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/Users/path/to/super/fun/graphs", "--router", "gg" ])
router = otp.getRouter()
r = otp.createRequest()
r.setDateTime(2016, 9, 8, 17, 0, 00) # departure date / time
r.setModes('BICYCLE') # modes to include - just biking for this case
r.setMaxTimeSec(max_travel_time) # max time allowed - e.g. 1 hour in this case
r.setClampInitialWait(0) # include any waiting time it output

# list of unique ids
ids = []

# list of the two output tables
oot_toto = []

qq = 0

# compute travel times from
for data in in_data:

    # origin,
    o_lat = float(data[0])
    o_lon = float(data[1])
    origin = [o_lat, o_lon]

    # set up routing with origin
    r.setOrigin(origin[0], origin[1]) # set origin
    spt = router.plan(r)

    # the output header of the road file:
    # oot_table = [['geoid','objectid','travel_time']]

    # output array for
    oot_table = []
    print time.time() - start_time
    with open("midpoints.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result = spt.eval(float(row['Y']),float(row['X'])) # set destination
            if result is not None:
                travel_time = result.getTime()
                oot_table.append([row['GEO_ID'],row['OBJECTID'],travel_time]) # the geo_id and objectid are from the network nodes
            else:
                oot_table.append([row['GEO_ID'],row['OBJECTID'],max_travel_time + 1])
            if row['GEO_ID'] not in ids:
                ids.append(row['GEO_ID'])

    oot_toto.append(oot_table)

    # if qq == 2:
    #     break
    qq += 1

print len(ids)


# sum values to/from each point
output = []
w = 0
while w < len(ids):
    tt = 0
    for oo in oot_toto:
        tt = tt + oo[w][2]
        gg = oo[w][0]
        obj = oo[w][1]
    output.append([gg,obj,tt])
    w += 1
print w


# write to csv - can do other outputs if you want
with open('ppa.csv', 'w') as csvw:
    writer = csv.writer(csvw)
    writer.writerow(['gg','oo','tt'])
    for out in output:
        writer.writerow(out)

# print computation time
print ("----------------")
print time.time() - start_time

# don't forget to print how much fun this was!
print "that was fun!"
