# OpenTripPlanner_analysis

The scripts in this repository use OpenTripPlanner (OTP) for batch transportation network computations.

Below briefly explains how to set up OTP, what the scripts input and return, and how to run them.

---

## Setting up OTP

OTP is an open source multi-model transportation routing engine ([official website](http://www.opentripplanner.org/), [online documentation](http://docs.opentripplanner.org/en/latest/)). It can be used to route via biking, driving, transit, and/or walking.

OpenTripPlanner is written in Java (find the executable .jar [here](http://maven.conveyal.com/org/opentripplanner/otp/)) and uses OpenStreeMap (as .pbf or .xml) and GTFS (as a .zip package) as inputs.

OpenStreetMap data can be grabbed via:
```
wget http://overpass-api.de/api/map?bbox=-80.9,43.0,-77.9,44.5
```

The latest version of the OTP executable .jar:
```
wget http://maven.conveyal.com.s3.amazonaws.com/org/opentripplanner/otp/1.1.0/otp-1.1.0-shaded.jar
```

GTFS is available through local transit agencies.

Put the osm.xml(or.pbf), GTFS.zip(s), and the OTP.jar into a directory and use the following commands to build a routable graph.

```shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --inMemory --analyst
```

The ```4``` in the ```-Xmx4G``` refers to how much memory should be alocated to the build.

Check out http://localhost:8080/ to test if it's routing properly.

---

## Scripting OTP

There are a couple ways to script OTP to perform batch routing analysis... 
1 - by storing it on disk. 
2 - by storing it on a local server. 
Storing on disk allows for faster batch calculations, while storing on a local server can return a wider range of information.

### 1 - graph on disk

Building the graph and storing on disk as a graph.obj
```shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --basePath /path/to/dir/ --analyst
```

Running scripts on OTP requires [Jython](http://www.jython.org/), an implementation of Python to run Java. There are two commands for running a Python script with Jython:

1 - By calling Jython:
```shell
jython -Dpython.path=otp.jar my_script.py
# or to include memory option
jython -J-Xmx8g -Dpython.path=otp.jar my_script.py
```

2 - Or by having executable jython.jar in the same directory:
```shell
java -Xmx4G -cp otp.jar:jython.jar org.opentripplanner.standalone.OTPMain --graphs . --script my_script.py
```

Here a few scripts that perform batch travel time computations.

#### OD_single.py
Computes a single travel time from an origin to a destination for specific travel modes and departure time. This is used as a basis for batch computations.

#### OD_multi.py
Computes travel times between two points looping over multiple departure times and for different input graphs.

#### Travel_time_matrix.py
Computes a matrix of travel times from a series of origins to a series of destinations for a specific departure time and travel mode(s).

#### Travel_time_cube.py
Computes three dimensional array of travel times (origins-destinations-departure time). This is essentially the same script as above, but set in a function that's called in a loop to compute over consecutive minutes in a set time period (e.g. every minute in an hour).

#### cumulative_access.py
Computes cumulative access scores for a set of points. e.g. the number of jobs reachable by specific mode, within a specific time window

#### parallel.py
Travel time computations can often be time intensive. This simple script allows for parallel processing by calling scripts via the subprocess and multiprocessing modules.

#### one_to_many.py
Computes the travel times from one point to a set of many points.

#### ppa.py
Computes potential path areas, the area accessible between two points for a specific time window.


### 2 - graph in a local server

The second way to script OpenTripPlanner is to send get requests to a graph stored in a local server. The results can be grabbed using Python and storing results as dictionary objects.

These scripts don't require Jython. They can be called with regular Python.

Just make sure there's an instance running in your local server.
```shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --inMemory --analyst
```
We can also do this with a local graph.obj

```shell
java -jar otp.jar --graphs graphfoldername --router routername --server --enableScriptingWebService
```

Here are a few examples...

#### get_trip_itinerary.py
Grabs trip information between pairs of points. This includes departure time, duration, stop identifiers, and transit vehicle numbers. Results get put into a .csv table.

#### grab_route_geometry.py
Returns the trip geometry between pairs of points as geojson LineStrings.

---
