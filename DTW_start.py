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

def run_heatmap(input):
    output = []
    process = subprocess.Popen('python3 auswertung1.py ' + input, stdout=subprocess.PIPE,
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
    pbns = ["pb"+str(i) for i in range(1,54) if i not in [6,23,50,53]] #, "pb35", "pb35_2"] welche dateien fehlen????
    todo = [pb + " " + al for pb in pbns for al in aliases]
    results = pool.map(run_dtw, todo)
    with open("DTW_log.txt", "a") as file:
        file.write("Log_from_DTW:DynTimeWarp at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")

def main_heatmap_multi():
    pool = ThreadPool(4)
    pbnlist = ["pb1", "pb1_2", "pb2", "pb3", "pb3_2", "pb4", "pb5", "pb5_2", "pb7", "pb7_2", "pb8", "pb9", "pb9_2",
               "pb10", "pb11", "pb11_2", "pb12", "pb13", "pb13_2", "pb14", "pb15",
               "pb15_2", "pb16", "pb17", "pb17_2", "pb18", "pb19", "pb19_2", "pb20", "pb21", "pb21_2", "pb22", "pb24",
               "pb25", "pb25_2", "pb26", "pb27", "pb27_2", "pb28", "pb29", "pb29_2", "pb30", "pb31", "pb31_2", "pb32",
               "pb33", "pb33_2", "pb34", "pb35", "pb35_2", "pb36", "pb37", "pb37_2", "pb38", "pb39", "pb39_2", "pb40",
               "pb41", "pb41_2", "pb42", "pb43", "pb43_2", "pb44", "pb45", "pb45_2", "pb46", "pb47", "pb47_2", "pb48",
               "pb49", "pb49_2", "pb51", "pb51_2", "pb52"]
    distances = ["euklid", "winkel", "winkellog"]
    aliases = ["Spot1", "Spot5", "GL1", "GL5", "BGL1", "BGL5"]
    todo = [pb + " " + al + " " + dist for pb in pbnlist for al in aliases for dist in distances]
    results = pool.map(run_heatmap, todo)
    with open("DTW_Heatmap_log.txt", "a") as file:
        file.write("Log_from_DTW:DynTimeWarp at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")



if __name__ == "__main__":
    #main2_multi()
    # plot_multi()
    main_heatmap_multi()