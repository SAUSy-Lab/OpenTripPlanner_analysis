import requests, polyline, csv, json, time, ast, datetime

start_time = time.time()
print time.time() - start_time

in_table = "home_campus_pairs.csv"

m = 29
while m < 60:

    if m < 10:

        minute = "0" + str(m)

    if m > 9:

        minute = str(m)

    csv_out_name = "transit_new/" + str(minute) + ".csv"


    f = 0
    c = 0
    out_array = [["HHkey", "duration", "walk_dist", "walk_time","initial_wait_time","transfer_time", "transit_time", "transfers"]]

    with open(in_table, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:

            print "----------------------"
            print m, c, row[0]

            c += 1

            if row[1] != "home_x":

                try:

                    x1 = str(row[1])
                    y1 = str(row[2])

                    x2 = str(row[3])
                    y2 = str(row[4])


                    url_string = "http://localhost:8080/otp/routers/default/plan?fromPlace=" + y1 + "%2C" + x1 +  "&toPlace=" + y2 + "%2C" + x2 + "&time=10%3A" + minute + "am&date=07-20-2016&mode=TRANSIT%2CWALK&maxWalkDistance=9999&arriveBy=false&wheelchair=false&locale=en"


                    # 43.714790281327886%2C-79.2498779296875&toPlace=43.640299091949906%2C-79.39441680908203

                    print url_string

                    page = requests.get(url_string)

                    line_coords = []
                    dic = json.loads(page.content)

                    duration = dic['plan']['itineraries'][0]['duration']
                    walk_dist = dic['plan']['itineraries'][0]['walkDistance']
                    walk_time = dic['plan']['itineraries'][0]['walkTime']
                    transit_time = dic['plan']['itineraries'][0]['transitTime']
                    wait_time = dic['plan']['itineraries'][0]['waitingTime']
                    transfers = dic['plan']['itineraries'][0]['transfers']

                    date_time = '20.07.2016 10:' + minute + ':00'
                    pattern = '%d.%m.%Y %H:%M:%S'
                    startepoch = int(time.mktime(time.strptime(date_time, pattern)))

                    start_trip_time = dic['plan']['itineraries'][0]['startTime'] / 1000

                    initial_wait_time = start_trip_time - startepoch

                    print start_trip_time
                    print startepoch
                    print initial_wait_time

                    out_row = [row[0],duration,walk_dist,walk_time,initial_wait_time,wait_time,transit_time,transfers]

                    out_array.append(out_row)

                except:

                    f += 1


            # if c > 10:
            #     break

    with open(csv_out_name, "w") as csvfile:

        writer = csv.writer(csvfile)
        for row in out_array:
            writer.writerow(row)

    m += 1



print "---------------"
print f
print time.time() - start_time
