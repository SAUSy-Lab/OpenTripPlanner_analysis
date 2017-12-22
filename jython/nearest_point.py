# ---------------------
# run via ...
# jython -Dpython.path=otp.jar nearest_point.py
# ---------------------

# returns least cost travel time from a set of points O to the closest point in another set of points D

from org.opentripplanner.scripting.api import *
import time
import csv

# time script
start_time = time.time()

# grab input points
in_points = 'points.csv'
in_data = []
with open(in_points, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for xy in reader:
        in_data.append(xy)
print in_data

# list of every output table
oot_toto = []

# initial load graph - have graphs store in "graphs" folder and routing set up
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/Users/path/to/graphs", "--router", "drgraph" ])
router = otp.getRouter()
r = otp.createRequest()
r.setDateTime(2016, 9, 8, 17, 0, 00) # departure date / time
r.setModes('WALK') # modes to include
r.setMaxTimeSec(1200) # time out (in seconds)- max travel time - e.g. 20 minutes max - greater distance, more time it takes to run
r.setClampInitialWait(0) # include any waiting time it output

# list of unique ids
ids = []

qq = 0

# compute travel times from set of points O
for data in in_data:

    # origins
    o_lat = float(data[1])
    o_lon = float(data[0])
    origin = [o_lat, o_lon]

    # set up routing with origin
    r.setOrigin(origin[0], origin[1]) # set origin
    spt = router.plan(r)

    # the output header of the road file:
    # oot_table = [['geoid','objectid','travel_time']]

    # output arrays
    oot_table = []
    
    # set of points D    
    with open("points.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result = spt.eval(float(row['Y']),float(row['X'])) # set destination
            if result is not None:
                travel_time = result.getTime()
                oot_table.append([row['GEO_ID'],row['OBJECTID'],travel_time])
            else:
                oot_table.append([row['GEO_ID'],row['OBJECTID'],1201])
            if row['GEO_ID'] not in ids:
                ids.append(row['GEO_ID'])

    oot_toto.append(oot_table)

    # # break for testing
    # if qq == 2:
    #     break
    qq += 1

print len(ids)


# grab just the lowest value for each point
output = []
w = 0
while w < len(ids):
    tt = 1202 # max value - can return this if no points were close to this
    for oo in oot_toto:
        if oo[w][2] < tt:
            tt = oo[w][2]

        gg = oo[w][0]
        obj = oo[w][1]
    output.append([gg,obj,tt])

    w += 1

print w


# write to csv
with open('metro_walk_sheds.csv', 'w') as csvw:
    writer = csv.writer(csvw)
    writer.writerow(['gg','oo','tt'])
    for out in output:
        writer.writerow(out)

# print computation time
print ("----------------")
print time.time() - start_time

# as usual, print that this was indeed fun!
print "that was fun!"
