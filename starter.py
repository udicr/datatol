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


def run_aw2(pbn):
    output = []
    process = subprocess.Popen('python3 auswertung2.py ' + pbn, stdout=subprocess.PIPE,
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
            todo.append(p + " " + d)
    print("Todo: ")
    print(todo)
    results = pool.map(run_aw1, todo)
    return results


def aw2_multi():
    pool = ThreadPool(4)
    pbns = ["pb1", "pb1_2", "pb2"]  # , "pb2", "pb3", "pb3_2", "pb4"]
    distances = ["euklid", "winkel", "winkellog"]
    aliases = ["Spot1", "Spot5", "GL1", "GL5", "BGL1", "BGL5", "Control1", "Control5"]
    todo = []
    for p in pbns:
        for a in aliases:
            for d in distances:
                todo.append(p + " " + a + " " + d)
    print("Todo: ")
    print(todo)
    results = pool.map(run_aw2, todo)
    return results


if __name__ == "__main__":
    #heatmap_multi()
    aw2_multi()