# computes travel time cube from origins (lat long in DA.csv)
# to destinations (TAZ_centroids.csv) for set time range

# run with ...
# java -Xmx4G -cp otp.jar:jython.jar org.opentripplanner.standalone.OTPMain --graphs . --script Travel_time_matrix.py
# jython -Dpython.path=otp.jar Travel_time_matrix.py

from org.opentripplanner.scripting.api import *
from org.opentripplanner.analyst.batch import BatchProcessor
from org.opentripplanner.scripting.api import OtpsEntryPoint
import time
import csv
from operator import itemgetter

print "cow!" # print cow!

# time for time
start_time = time.time()

# function for single OD matrix
def OD_matrix(day,hour,minute):

    print "start" + "_" + str(day) + "_" + str(hour) + "_" + str(minute)

    # initial load graph
    otp = OtpsEntryPoint.fromArgs([ "--graphs", "/path/to/dir/graphs", "--router", "ttc_realtime" ])

    router = otp.getRouter()

    # basic routing stuff - can set more via json
    r = otp.createRequest()
    r.setDateTime(2016, 7, day, hour, minute, 00)
    r.setModes('WALK, TRANSIT')
    r.setMaxTimeSec(3600)
    r.setClampInitialWait(0)
    r.setMaxWalkDistance(5000)

    # out lists
    out_table = []
    origin_list = []
    destination_list = []
    # grab lists of origina and destinations
    with open('da.csv', 'rb') as csv_da:
        da_reader = csv.DictReader(csv_da)
        for da in da_reader:
            if int(da['DAuid']) not in origin_list:
                origin_list.append(int(da['DAuid']))
            with open('TAZ_centroids.csv', 'rb') as csv_TAZ:
                TAZ_reader = csv.DictReader(csv_TAZ)
                for row in TAZ_reader:
                    if int(row['GTA06']) not in destination_list:
                        destination_list.append(int(row['GTA06']))

    # loop over input da and use as origins
    with open('da.csv', 'rb') as csv_da:
        da_reader = csv.DictReader(csv_da)
        d = 0
        for da in da_reader:
            # add origin
            d_lat = float(da['DAlat'])
            d_lon = float(da['DAlong'])
            # set up router for point
            r.setOrigin(d_lat, d_lon)
            spt = router.plan(r)
            # loop over input supers and use as destinations
            with open('TAZ_centroids.csv', 'rb') as csv_super:
                super_reader = csv.DictReader(csv_super)
                s = 0
                for row in super_reader:
                    out_row = []
                    # add dest
                    lat = float(row['Y'])
                    lon = float(row['X'])
                    # solve
                    result = spt.eval(lat,lon)
                    if result is not None:
                        # get time
                        travel_time = result.getTime()
                        # output row to array
                        out_row = [int(da['Geo_ID']),int(da['DAuid']),int(row['ID']),int(row['GTA06']),int(travel_time)]
                        out_table.append(out_row)
                    s += 1

            d += 1
            print '---------'
            print d
            print time.time() - start_time
            print '---------'

    # sort out_table
    out_table = sorted(out_table, key=itemgetter(0,1))

    # grab list of all origins and destinations - can bring in externally if needed
    origin_list = sorted(origin_list)
    destination_list = sorted(destination_list)

    # set up matrix
    matrix = [[0 for x in range(len(destination_list) + 1)] for y in range(len(origin_list) + 1)]

    print "------------"

    # code in matrix values
    for tr in out_table:
        matrix[tr[0]][tr[2]] = tr[4]

    # add row and column names
    x = 0
    while x < len(destination_list):
        x += 1
        matrix[0][x] = destination_list[x-1]
    x = 0
    while x < len(origin_list):
        x += 1
        matrix[x][0] = origin_list[x-1]

    matrix[0][0] = hour * 100 + minute

    # out to csv
    file_name = "r_" + "7_" + str(day) + "_" + str(hour) + "_" + str(minute) + ".csv"
    with open(file_name, 'wb') as csv_walk:
        writer = csv.writer(csv_walk)
        for tt in matrix:
            writer.writerow(tt)

# compute cube for every minute in an hour
m = 0
while m < 60:
    OD_matrix(4,20,m)
    m += 1
