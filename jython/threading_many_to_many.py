# computes travel times between p number of lat lon origins and destinations
# uses a queue to thread jobs from origins (orig CSV) to destinations (dest CSV) 

print "let's start"

from org.opentripplanner.scripting.api import OtpsEntryPoint
from org.opentripplanner.scripting.api import *
import time
import math
import random
import csv
import subprocess
import threading
from operator import itemgetter
print(time.time())

start_time = time.time()

### Data organization and input ###
### Verify these fields are filled in properly and alter as needed ##
max_threads = 5
p = '10k' # refers the naming convention - update as needed
orig = 'points_{}'.format(p) # origin CSV
dest = 'points_{}'.format(p) # destination CSV

orig_list = []
with open('./{}.csv'.format(orig), 'rb') as csv_orig:
    orig_reader = csv.DictReader(csv_orig)
    for i in orig_reader:
        origin = (int(i['FID']),float(i['lat']),float(i['long']))
        orig_list.append(origin)


#### LOAD GRAPH INDEPENDENT OF FUNCTION #######
print "load the graph"
otp = OtpsEntryPoint.fromArgs([ "--graphs", "./graph", "--router", "schedule" ])
## must updated to reflect own file structure 
###############################################

master_table = []

print "defining function"
def OD_thread(uid,lat,lon):

    router = otp.getRouter()

    # basic routing parameters
    # updated as needed
    r = otp.createRequest()
    r.setOrigin(lat,lon)
    r.setDateTime(2019,12,30,8,00,00) # may need to change date/time
    r.setModes("WALK, TRANSIT") # add modes if addit. needed
    r.setMaxTimeSec(2700)
    r.setClampInitialWait(0) # include wait times at stops
    r.setMaxWalkDistance(5000) 
    time_of_day = "8:00 am" # not necessary, but included in output CSV for future reference 

    # destination list
    destination_list = []

    with open("./{}.csv".format(dest), "rb") as csv_dest:
        dest_reader = csv.DictReader(csv_dest)
        for j in dest_reader:
            destination_list.append(int(j['FID']))

    # begin routing
    spt = router.plan(r)
    #if spt is None: continue

    # loop over desintations
    d = 0
    with open("./{}.csv".format(dest), "rb") as csv_dest:
        dest_reader = csv.DictReader(csv_dest)
        for j in dest_reader:
            if uid == j['FID']:
                continue
            out_row = []

            # add destination
            d_lat = float(j['lat'])
            d_lon = float(j['long'])

            # solve
            result = spt.eval(d_lat, d_lon)
            if result is not None:
                travel_time = result.getTime()
                out_row = [int(uid),int(j['FID']),str(time_of_day),int(travel_time)]
                master_table.append(out_row)

            d += 1
            print "__________"
            print d
            print time.time() - start_time
            print "__________"

print "end of function definition. Time to map origins and run analysis"

###############
from Queue import Queue

#set up queue to hold all origins
q = Queue(maxsize=0)

#use many threads
num_threads = min(100, len(orig_list))

#populate queue with tasks
results = [{} for i in orig_list];

#load queue with the origins to fetch and the IDs
for i in range(len(orig_list)):
    q.put((orig_list[i])) 

#thread for queue processing
def crawl(q, result):
    while not q.empty():
        work = q.get()
        try:
            OD_thread(work[0],work[1],work[2])
        except:
            print "issue with queue"
        q.task_done()
    return True

for i in range(num_threads):
    print "Starting thread {}".format(i)
    t = threading.Thread(target=crawl, args = (q, results))
    t.setDaemon(True)
    t.start()

q.join() 

master_table = sorted(master_table, key=itemgetter(0,1))
file_name = "./{}_p_matrix_45min.csv".format(p)
with open(file_name, "wb") as csv_out:
    writer = csv.writer(csv_out)
    writer.writerow(['orig_FID','dest_FID','DepTime','TT'])
    if len(master_table) == 0:
        print "table empty, try again"
    else:
        for row in master_table:
            writer.writerow(row)
        print "csv written to file"
        
pro_time = time.time() - start_time

print "Calculations complete. It took: {} secs".format(pro_time)

###################
