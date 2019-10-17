from multiprocessing.dummy import Pool as ThreadPool
import datetime
import subprocess
import sys


def run_aw1(pbn):
    output = []
    process = subprocess.Popen('python3 auswertung1.py ' + pbn, stdout=subprocess.PIPE,
                               cwd=".", shell=True)
    for line in iter(process.stdout.readline, b''):
        l = line.decode('utf-8')
        sys.stdout.write(l)
        output.append(l.rstrip())

    return output


def heatmap_multi():
    pool = ThreadPool(3)
    pbns = ["pb1", "pb1_2", "pb2"]  # , "pb2", "pb3", "pb3_2", "pb4"]
    distances = ["euklid", "winkel", "winkellog"]
    todo = []
    for p in pbns:
        for d in distances:
            todo.append(p+" "+d)
    print("Todo: ")
    print(todo)
    results = pool.map(run_aw1, todo)
    return results


heatmap_multi()