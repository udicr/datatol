from multiprocessing.dummy import Pool as ThreadPool
import datetime
import subprocess
import sys


def run_dtw(pbn):
    output = []
    process = subprocess.Popen('python DTW.py ' + pbn, stdout=subprocess.PIPE,
                               cwd=".", shell=True)
    for line in iter(process.stdout.readline, b''):
        l = line.decode('utf-8')
        sys.stdout.write(l)
        output.append(l.rstrip())

    return output


def plot_dtw(pbn):
    output = []
    process = subprocess.Popen('python DTW.py ' + pbn + " plot", stdout=subprocess.PIPE,
                               cwd=".", shell=True)
    for line in iter(process.stdout.readline, b''):
        l = line.decode('utf-8')
        sys.stdout.write(l)
        output.append(l.rstrip())

    return output


def main_multi():
    pool = ThreadPool(4)
    pbns = ["pb10", "pb11", "pb12", "pb13"]
    results = pool.map(run_dtw, pbns)
    with open("DTW_log.txt", "a") as file:
        file.write("Log_from_DTW:DynTimeWarp at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")


def plot_multi():
    pool = ThreadPool(4)
    pbns = ["pb10","pb11_2","pb11","pb13_2","pb13","pb12"]
    results = pool.map(plot_dtw, pbns)
    with open("DTW_plotlog.txt", "a") as file:
        file.write("Log_from_DTW:Plot at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")

if __name__ == "__main__":
    main_multi()
    plot_multi()
