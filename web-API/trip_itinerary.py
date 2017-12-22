# grabs trip information between pairs of points
# for different times of day using opentriplanner

# outputs as a csv file with this info:
# ['From','To','Depart_time','Duration','stop_id_1','stop_id_2','leg_routes','leg_durations','headsigns']

import requests, polyline, csv, json, time, ast, pprint
from datetime import datetime

start_time = time.time()

gtfs = "schedule" # realtime

def grab_iten(url):

    # try
    try:
        # request data
        page = requests.get(url_string)

        # convert result into dictionary
        dic = json.loads(page.content)

        # number of legs in journey
        leg_len = len(dic['plan']['itineraries'][0]['legs'])

        # grab route numbers, headsigns, and travel times for each leg
        # also grab starting and ending stop ids
        l = 0
        leg_list = []
        headsign_list = []
        times_list = []
        while l < leg_len:
            leg_info = dic['plan']['itineraries'][0]['legs'][l]
            l_mode = leg_info['mode']
            # for a single - just walking - leg
            if leg_len == 1:
                l_routename = 'W'
                leg_list.append(l_routename)
                l_stop1 = -1
                l_stop2 = -1
                l_time = (leg_info['endTime'] - leg_info['startTime']) / 1000
                times_list.append(l_time)
            # for any multi leg trip - i.e. with transit
            else:
                # first walking leg
                if l_mode == 'WALK' and l == 0:
                    l_routename = 'W'
                    leg_list.append(l_routename)
                    l_stop1 = str(leg_info['to']['stopId'])
                    l_stop1 = int(l_stop1.split(":")[1])
                    l_time = (leg_info['endTime'] - leg_info['startTime']) / 1000
                    times_list.append(l_time)
                # last walking leg
                elif l_mode == 'WALK' and l == (leg_len - 1):
                    l_routename = 'W'
                    leg_list.append(l_routename)
                    l_stop2 = str(leg_info['from']['stopId'])
                    l_stop2 = int(l_stop2.split(":")[1])
                    l_time = (leg_info['endTime'] - leg_info['startTime']) / 1000
                    times_list.append(l_time)
                # any intermediary walking leg
                elif l_mode == 'WALK':
                    l_routename = 'W'
                    leg_list.append(l_routename)
                    l_time = (leg_info['endTime'] - leg_info['startTime']) / 1000
                    times_list.append(l_time)
                # transit leg
                else:
                    l_routename = str(leg_info['route'])
                    l_headsign = str(leg_info['headsign'])
                    headsign_list.append(l_headsign)
                    leg_list.append(l_routename)
                    l_time = (leg_info['endTime'] - leg_info['startTime']) / 1000
                    times_list.append(l_time)

            l += 1

        duration = (dic['plan']['itineraries'][0]['endTime'] - dic['plan']['date']) / 1000

        # from, to, dep_tim, duration, stop_1, stop_2, iten
        out_row = [o_id,d_id,depart_time,duration,l_stop1,l_stop2,leg_list,times_list,headsign_list]

    except:
        print "fail"
        out_row = [o_id,d_id,depart_time,-1,-1,-1,['FAIL'],['FAIL']]

    return out_row

# grabing list of start times with format of:
# [month, day, hour, minute]
depart_times = []
days = [[8,30],[8,31]] # e.g. for two days at the end of august
for day in days:
    h = 0
    while h < 24:
        m = 0
        while m < 60:
            d_time = [day[0],day[1],h,m]
            depart_times.append(d_time)
            m += 1
        h += 1

# input OD pairs using this csv format:
# ID1, ID2, X1, Y1, X2, Y2

pair_array = []
with open("od_pairs.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    x = 0
    for row in reader:
        if x != 0:
            pair_array.append(row)
        x += 1


# loop over each pair of locations
for pair in pair_array:

    # set up where the output data goes
    out_array = []

    # iten for going from A to B:

    o_id = pair[0]
    o_lon = pair[2]
    o_lat = pair[3]
    d_id = pair[1]
    d_lon = pair[4]
    d_lat = pair[5]

    for depart_time in depart_times:
        print depart_time

        # turn times into strings

        if depart_time[0] < 10:
            d_mon = "0" + str(depart_time[0])
        else:
            d_mon = str(depart_time[0])
        if depart_time[1] < 10:
            d_day = "0" + str(depart_time[1])
        else:
            d_day = str(depart_time[1])

        d_time = str(depart_time[2]) + ":" + str(depart_time[3])
        d_time = datetime.strptime(d_time, "%H:%M")
        d_time = str(d_time.strftime("%I:%M %p"))
        d_time = d_time.replace(" ", "")

        url_string = "http://localhost:8080/otp/routers/default/plan?fromPlace=" + str(o_lat) + "%2C" + str(o_lon) + "&toPlace=" + str(d_lat) + "%2C" + str(d_lon) + "&time=" + d_time + "&date=" + d_mon + "-" + d_day + "-2016&mode=WALK,TRANSIT&maxWalkDistance=5000&arriveBy=false&wheelchair=false&locale=en"

        out_row = grab_iten(url_string)

        out_array.append(out_row)

        print out_row

        print '-----'
        print '-----'

    # iten for going from B to A:

    d_id = pair[0]
    d_lon = pair[2]
    d_lat = pair[3]
    o_id = pair[1]
    o_lon = pair[4]
    o_lat = pair[5]

    for depart_time in depart_times:
        print depart_time

        # turn times into strings

        if depart_time[0] < 10:
            d_mon = "0" + str(depart_time[0])
        else:
            d_mon = str(depart_time[0])
        if depart_time[1] < 10:
            d_day = "0" + str(depart_time[1])
        else:
            d_day = str(depart_time[1])

        d_time = str(depart_time[2]) + ":" + str(depart_time[3])
        d_time = datetime.strptime(d_time, "%H:%M")
        d_time = str(d_time.strftime("%I:%M %p"))
        d_time = d_time.replace(" ", "")

        url_string = "http://localhost:8080/otp/routers/default/plan?fromPlace=" + str(o_lat) + "%2C" + str(o_lon) + "&toPlace=" + str(d_lat) + "%2C" + str(d_lon) + "&time=" + d_time + "&date=" + d_mon + "-" + d_day + "-2016&mode=WALK,TRANSIT&maxWalkDistance=5000&arriveBy=false&wheelchair=false&locale=en"

        out_row = grab_iten(url_string)

        out_array.append(out_row)

        print out_row

        print '-----'
        print '-----'

    # special name for a special csv
    csv_name = "out_csvs/PP_" + pair[0] + '_' + pair[1] + '.csv'

    # write to csv
    with open(csv_name, 'w') as csvwrite:
        writer = csv.writer(csvwrite)
        writer.writerow(['From','To','Depart_time','Duration','stop_id_1','stop_id_2','leg_routes','leg_durations','headsigns'])
        for hamster in out_array:
            writer.writerow(hamster)


print "+" * 10
print time.time() - start_time
