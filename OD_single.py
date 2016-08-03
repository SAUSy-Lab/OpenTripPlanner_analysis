# computes travel time from an origin to a destination
# for specific travel modes and departure time

# run with...
# jython -Dpython.path=otp.jar OD_single.py

from org.opentripplanner.scripting.api import *
import time
import csv

# time script
start_time = time.time()

# origin
origin = [float(43.664200), float( -79.411280)]
dest = [float(43.801744), float(-79.296474)]

# initial load graph - have graphs store in "graphs" folder
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/path/to/dir/graphs", "--router", "schedule" ])

# set up routing
router = otp.getRouter()
r = otp.createRequest()
r.setDateTime(2016, 7, 9, 8, 20, 00) # departure date / time
r.setModes('TRANSIT, WALK') # modes to include
r.setMaxTimeSec(50000) # time out (in seconds)
r.setClampInitialWait(0) # include any waiting time it output
r.setOrigin(origin[0], origin[1]) # set origin
spt = router.plan(r)
result = spt.eval(dest[0],dest[1]) # set destination

# print result
print ("----------------")
if result is not None:
    travel_time = result.getTime()
    print travel_time
else:
    print ":("

# print computation time
print ("----------------")
print time.time() - start_time


print "that was fun!"
