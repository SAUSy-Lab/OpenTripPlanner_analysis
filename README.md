## OpenTripPlanner_analysis

The scripts in this repository use of OpenTripPlanner (OTP) to analyze urban transportation systems.

OTP is an open source multi-model transportation routing platform ([official website](http://www.opentripplanner.org/), [online documentation](http://docs.opentripplanner.org/en/latest/)).

Below is a brief outline of how to set up OTP and how it can be scripted for transit analysis.

---

### Setting up OTP

OpenTripPlanner is written in Java (find the executable .jar [here](http://maven.conveyal.com/org/opentripplanner/otp/)) and uses OpenStreeMap (as .pbf or .xml) and GTFS (as a .zip package) as inputs.

OpenStreetMap data can be grabbed via:
```
wget http://overpass-api.de/api/map?bbox=-80.9,43.0,-77.9,44.5
```

The latest version of the OTP executable .jar:
```
wget http://maven.conveyal.com.s3.amazonaws.com/org/opentripplanner/otp/1.0.0/otp-1.0.0-shaded.jar
```

GTFS is available through local transit agencies.

Put the osm.xml(or.pbf), GTFS.zip(s), and the OTP.jar into a directory and use the following commands to build a routable graph.

```shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --inMemory --analyst
```

Check out http://localhost:8080/ to test if it's routing properly.

---

## Scripting OTP

There are a couple ways to script OTP to perform batch routing analysis...
1 - by storing it on disk
2 - by storing it on a local server
Storing on desk allows for faster batch calculations, while storing on a local server has more options.

###1 - on disk

Building the graph and storing on disk as a graph.obj
```shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --basePath /path/to/dir/ --analyst
```

Running scripts on OTP requires [Jython](http://www.jython.org/), an implementation of Python to run Java. There are two commands for running a Python script with Jython:

1 - By calling Jython:
```shell
jython -Dpython.path=otp.jar my_script.py
```

2 - Or by having executable jython.jar in the same directory:
```shell
java -Xmx4G -cp otp.jar:jython.jar org.opentripplanner.standalone.OTPMain --graphs . --script my_script.py
```

The ```4``` in the ```-Xmx4G``` refers to how much memory should be alocated to the build.

Here a few scripts that perform batch travel time computations  

#### OD_single.py
Computes a single travel time from an origin to a destination for specific travel modes and departure time. Used as a basis for batch computations.

#### OD_multi.py
Computes travel times between two points looping over multiple departure times and for different input graphs.

#### Travel_time_matrix.py
Computes a matrix of travel times from a series of origins to a series of destinations.

#### Travel_time_cube.py
Computes three dimensional array of travel times (origins-destinations-departure time). This is essentially the same script as above, but set in a function that's called in a loop compute over consecutive minutes in a set time period (e.g. every minute in an hour).

#### parallel.py
Travel time computations can often be time intensive. This simple script allows for parallel processing calling scripts via the subprocess and multiprocessing modules.

#### one_to_many.py
Computes the travel times from one point to a set of many points.

#### ppa.py
Computes Potential Path Areas, the area accessible between two points for a specific time window.

###2 - in a local server.

The second way to script OpenTripPlanner

These scripts don't require Jython. They can be called with regular Python.

Just make sure there's an instance running in your local server.
```shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --inMemory --analyst
```

The locally served graph can be return results via get requests. The results can be grabbed using Python and then stored as dictionary objects.

Here are a few examples...

#### get_trip_itinerary.py
Grabs trip information between pairs of points. This includes departure time, duration, stop identifiers, and transit vehicle numbers. Results get put into a .csv table.

#### grab_route_geometry.py
Returns the trip geometry between pairs of points as geojson LineStrings.

---
