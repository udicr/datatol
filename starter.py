from multiprocessing.dummy import Pool as ThreadPool
import datetime
import subprocess
import sys

def run_aw1(pbn):
    output = []
    process = subprocess.Popen('python auswertung1.py ' + pbn, stdout=subprocess.PIPE,
                               cwd=".", shell=True)
    for line in iter(process.stdout.readline, b''):
        l = line.decode('utf-8')
        sys.stdout.write(l)
        output.append(l.rstrip())

    return output
def heatmap_multi():
    pool = ThreadPool(4)
    pbns = ["pb1", "pb1_2","pb2","pb3"]  # , "pb2", "pb3", "pb3_2", "pb4"]
    results = pool.map(run_aw1, pbns)
    return results