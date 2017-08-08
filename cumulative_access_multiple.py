# computes multiple cumulative accessiblity for a set of points

# i.e. the total number of opportunities (e.g. jobs) accessible from a point
# for several time windows, and for multiple start times

# run via ...
# jython -Dpython.path=otp.jar jobs_access.py
# jython J-Xmx8g -Dpython.path=otp.jar jobs_access.py

from org.opentripplanner.scripting.api import *
import time
import csv

start_time = time.time()

# job counts and destinations
jobs = []
with open("TAZ_Emp_dos.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = int(row["GTA06"])
        jobs_count = int(row["wrkdest24h"])
        jobs.append([id,jobs_count])
print len(jobs)

# origin locations
origins = []
with open("db_centroids.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x = row['X']
        y = row['Y']
        id = row['dbuid']
        origins.append([x,y,id])

print len(origins)

# destination coordinates
destinations = []
with open("TAZ_points.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x = row['X']
        y = row['Y']
        id = row['GTA06']
        destinations.append([x,y,id])

print len(destinations)

# enter the graph
otp = OtpsEntryPoint.fromArgs([ "--graphs", "graphs", "--router", "ggh" ])
router = otp.getRouter()
r = otp.createRequest()



loop_start_time = time.time()
print loop_start_time - start_time

# loop over every minute in the hour
minute = 0
while minute < 60:

    # basic routing setup
    r.setDateTime(2016, 7, 20, 8, minute, 00) # departure date / time
    r.setModes('WALK,TRANSIT') # modes to include
    r.setMaxTimeSec(3600) # max travel time threshold T
    r.setMaxWalkDistance(5000)
    r.setClampInitialWait(0)


    print "----------------"
    print minute


    scores_id = []
    # loop over each origin point
    for orig in origins:

	try:
		r.setOrigin(float(orig[1]), float(orig[0])) # set origin
		spt = router.plan(r)

		inside_dests_60 = []
		inside_dests_45 = []
		inside_dests_30 = []

		# loop over each destinatin point
		for dest in destinations:

		    #print float(row[1]),float(row[0])
		    result = spt.eval(float(dest[1]),float(dest[0]))

		    if result is not None:
		        # if time is less than threshold
		        inside_dests_60.append(dest[2])

		        tt = result.getTime()
		        if tt <= 2700:
		            inside_dests_45.append(dest[2])
		        if tt <= 1800:
		            inside_dests_30.append(dest[2])


		# sum score for each origin
		score60 = 0
		for row in inside_dests_60:
		    for job in jobs:
		        if int(row) == int(job[0]):
		            #print score
		            score60 = score60 + job[1]
		            break
		
		# those just under 45 mins
		score45 = 0
		for row in inside_dests_45:
		    for job in jobs:
		        if int(row) == int(job[0]):
		            #print score
		            score45 = score45 + job[1]
		            break

		# those just under 30 mins
		score30 = 0
		for row in inside_dests_30:
		    for job in jobs:
		        if int(row) == int(job[0]):
		            #print score
		            score30 = score30 + job[1]
		            break

		# append to output
		scores_id.append([orig[2],score60,score45,score30])

		print minute, orig[2], "okay"
	except:
		print minute, orig[2], "FAIL!"
		scores_id.append([orig[2],-1,-1,-1])

    # write csv for each minute - doing each incase of failure - could do outside while loop
    with open("out_times/" + str(minute) + ".csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in scores_id:
            writer.writerow(row)

    minute += 1
    print time.time() - loop_start_time

    

# finish the loop and
print "moooooo"
