# computes cumulative accessiblity for a set of points

# i.e. the total number of opportunities (e.g. jobs) accessible from a point
# given a certain time window, and for multiple start times

# run via ...
# jython -Dpython.path=otp.jar jobs_access.py


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
with open("geocoded.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x = row['X']
        y = row['Y']
        id = row['ID']
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
otp = OtpsEntryPoint.fromArgs([ "--graphs", "graphs", "--router", "gta" ])
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
    r.setMaxTimeSec(2700) # max travel time threshold T
    r.setMaxWalkDistance(5000)
    r.setClampInitialWait(0)


    print "----------------"
    print minute


    scores_id = []
    # loop over each origin point
    for orig in origins:


        r.setOrigin(float(orig[1]), float(orig[0])) # set origin
        spt = router.plan(r)

        inside_dests = []
        
        
        # loop over each destinatin point
        for dest in destinations:

            #print float(row[1]),float(row[0])
            result = spt.eval(float(dest[1]),float(dest[0]))

            if result is not None:
                # if time is less than threshold
                inside_dests.append(dest[2])

        # sum score for each origin
        score = 0
        for row in inside_dests:
            for job in jobs:
                if int(row) == int(job[0]):
                    #print score
                    score = score + job[1]

        # append to output
        scores_id.append([orig[2],score])

    # write csv for each minute - doing each incase of failure - could do outside while loop
    with open("out_person_times/" + str(minute) + ".csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in scores_id:
            writer.writerow(row)

    minute += 1
    print time.time() - loop_start_time

# finish the loop and
print "moooooo"
