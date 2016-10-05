# outputs travel times from one point to many points
# ouput includes ID of input destinations

from org.opentripplanner.scripting.api import *
import time
import csv

# time script
start_time = time.time()

# origin location
origin = [float(43.2), float(-79.2)]

# initial load graph - have graphs store in "graphs" folder
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/path/graphs", "--router", "router_name" ])

# set up routing
router = otp.getRouter()
r = otp.createRequest()
r.setDateTime(2016, 9, 8, 17, 0, 00) # departure date / time
r.setModes('BICYCLE') # modes to include
r.setMaxTimeSec(50000) # time out (in seconds)
r.setClampInitialWait(0) # include any waiting time it output
r.setOrigin(origin[0], origin[1]) # set origin
spt = router.plan(r)

# setting up output table with header in place
oot_table = [['geoid','objectid','travel_time']]

# print time for fun!
print time.time() - start_time

# open input and do the routing
with open("midpoints.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        result = spt.eval(float(row['Y']),float(row['X'])) # set destination
        if result is not None:
            travel_time = result.getTime()
            # geo_id and objectid go into output table
            oot_table.append([row['GEO_ID'],row['OBJECTID'],travel_time])
        else:
            print ":("
            oot_table.append([row['GEO_ID'],row['OBJECTID'],0])

# output csv name
with open('m_bike.csv', 'w') as csvw:
    writer = csv.writer(csvw)
    for oo in oot_table:
        writer.writerow(oo)

# print computation time - again for fun!
print ("----------------")
print time.time() - start_time

# mention how much fun that was!
print "that was fun!"
