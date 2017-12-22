import multiprocessing
from subprocess import call

def run_rabbit_run(i):
    print "running", i

    call(["jython", "-Dpython.path=otp.jar", i])

    # call(["java", "-Xmx4G", "-cp", "otp.jar:jython.jar", "org.opentripplanner.standalone.OTPMain", "--graphs", ".", "--script", i])

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    data = ("t1.py","t2.py","t3.py","t4.py") # call in parallel
    # data = (["t1.py"]) # single for testing
    pool.map(run_rabbit_run, data)
    pool.close()
