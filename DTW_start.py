from multiprocessing.dummy import Pool as ThreadPool
import datetime
import subprocess
import sys

aliases = [
    "Spot1",
    "Spot2",
    "Spot3",
    "Spot4",
    "Spot5",
    "Spot6",
    "Spot7",
    "Spot8",
    "GL1",
    "GL2",
    "GL3",
    "GL4",
    "GL5",
    "GL6",
    "GL7",
    "GL8",
    "BGL1",
    "BGL2",
    "BGL3",
    "BGL4",
    "BGL5",
    "BGL6",
    "BGL7",
    "BGL8"
]


def run_dtw(input):
    output = []
    process = subprocess.Popen('python3 DTW.py ' + input, stdout=subprocess.PIPE,
                               cwd=".", shell=True)
    for line in iter(process.stdout.readline, b''):
        l = line.decode('utf-8')
        sys.stdout.write(l)
        output.append(l.rstrip())

    return output


def plot_dtw(pbn):
    output = []
    process = subprocess.Popen('python3 DTW.py ' + pbn + " plot", stdout=subprocess.PIPE,
                               cwd=".", shell=True)
    for line in iter(process.stdout.readline, b''):
        l = line.decode('utf-8')
        sys.stdout.write(l)
        output.append(l.rstrip())

    return output


def main_multi():
    pool = ThreadPool(3)
    pbns = ["pb13"]
    results = pool.map(run_dtw, pbns)
    with open("DTW_log.txt", "a") as file:
        file.write("Log_from_DTW:DynTimeWarp at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")


def plot_multi():
    pool = ThreadPool(4)
    pbns = ["pb10", "pb11_2", "pb11", "pb13_2", "pb13", "pb12"]
    results = pool.map(plot_dtw, pbns)
    with open("DTW_plotlog.txt", "a") as file:
        file.write("Log_from_DTW:Plot at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")


def main2_multi():
    pool = ThreadPool(4)
    pbns = ["pb45", "pb46", "pb47", "pb48"] #, "pb35", "pb35_2"] welche dateien fehlen????
    todo = [pb + " " + al for pb in pbns for al in aliases]
    results = pool.map(run_dtw, todo)
    with open("DTW_log.txt", "a") as file:
        file.write("Log_from_DTW:DynTimeWarp at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")


if __name__ == "__main__":
    main2_multi()
    # plot_multi()
