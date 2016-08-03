## OpenTripPlanner_analysis

OpenTripPlanner is an open source multi-model transportation routing platform ([official website](http://www.opentripplanner.org/), [online documentation](http://docs.opentripplanner.org/en/latest/)).

The scripts in this repository make use of OpenTripPlanner for batch travel time computations for analysis of urban transportaiton systems.

---

### Setting up OTP

OpenTripPlanner is written in Java (find the executable .jar [here](http://maven.conveyal.com/org/opentripplanner/otp/)) and uses OpenStreeMap (as .pbf or .xml) and GTFS (as a .zip package) as inputs. Put these three into a directory and use the following commands to build a routable graph.

Command for building a graph and storing as graph.obj:
'''shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --basePath /path/to/dir/ --analyst
'''

Command for building a graph and putting it in a local server:
'''shell
java -Xmx4G -jar otp.jar --build /path/to/dir/ --inMemory --analyst
'''

Running scripts on OTP requires [Jython](http://www.jython.org/), an implementation of Python to run Java. There are two commands for running a Python script with Jython:

1 - By calling Jython:
'''shell
jython -Dpython.path=otp.jar my_script.py
'''

2 - Or by having executable jython.jar in the same directory:
'''shell
java -Xmx4G -cp otp.jar:jython.jar org.opentripplanner.standalone.OTPMain --graphs . --script my_script.py
'''

---

### Scripting OTP

#### OD_single.py
Computes single travel time from an origin to a destination for specific travel modes and departure time. Used as a basis for batch computations.

#### OD_multi.py
Computes travel times between two points looping over multiple departure times and for different input graphs.

#### Travel_time_matrix.py
Computes a matrix of travel times from a series of origins to a series of destinations.

#### Travel_time_cube.py
Computes multiple travel times cubes. This is essentially the same script as above, but set in function that's called in a loop compute over consecutive minutes in a set time period.

#### parallel.py
Travel time computations can often be time intensive. This simple script allows for parallel processing calling scripts via the subprocess and multiprocessing modules.
