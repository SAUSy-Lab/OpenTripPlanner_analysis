# computes travel time between two points for every minute
# between set time range and for two different graphs

# run with...
# jython -Dpython.path=otp.jar OD_multiple.py

from org.opentripplanner.scripting.api import *
import time
import csv

# origin and destination to analyze
origin = [float(43.757937), float(-79.315366)]
dest = [float(43.651911), float(-79.382175)]

# out lists and hours to compute
sched_list = [] # output list for one graph
real_mon = [] # output list for another graph
hours = [7,8] # hours to compute

# running on one graph
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/path/to/dir", "--router", "subgraph_name" ])
router = otp.getRouter()
for h in hours:
    m = 0
    while m < 60: # for each minute in each hour
        r = otp.createRequest()
        r.setDateTime(2016, 7, 18, h, m, 00)
        r.setModes('TRANSIT, WALK')
        r.setMaxTimeSec(4200)
        r.setOrigin(origin[0], origin[1])
        r.setClampInitialWait(0)
        spt = router.plan(r)
        result = spt.eval(dest[0],dest[1])
        print ("----------------")
        if result is not None:
            travel_time = result.getTime()
            print travel_time
            real_mon.append(travel_time)
        else:
            print ":("
            real_mon.append(8008135)
        print ("----------------")
        print time.time() - start_time
        m += 1


# and for the second graph ...
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/path/to/dir", "--router", "subgraph_name_2" ])
router = otp.getRouter()
for h in hours:
    m = 0
    while m < 60:
        r = otp.createRequest()
        r.setDateTime(2016, 7, 18, h, m, 00)
        r.setModes('TRANSIT, WALK')
        r.setMaxTimeSec(4200)
        r.setOrigin(origin[0], origin[1])
        r.setClampInitialWait(0)
        spt = router.plan(r)
        result = spt.eval(dest[0],dest[1])
        print ("----------------")
        if result is not None:
            travel_time = result.getTime()
            print travel_time
            sched_list.append(travel_time)
        else:
            print ":("
            sched_list.append(8008135)
        print ("----------------")
        print time.time() - start_time
        m += 1

# write outputs to a csv for comparison of travel times between two graphs
with open('out.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    q = 0
    while q < 120:
        writer.writerow([sched_list[q], real_mon[q])
        q += 1
