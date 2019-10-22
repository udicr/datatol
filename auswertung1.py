import pandas as pd
import numpy as np
from Pathmap import Pathmap
from multiprocessing.dummy import Pool as ThreadPool
import datetime
import subprocess
import sys
import csv
from distances import *
import statistics

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
    "BGL8",
    "Control1",
    "Control2",
    "Control3",
    "Control4",
    "Control5",
    "Control6",
    "Control7",
    "Control8",
]


# pbn = "pb1_2"

# pr = pbn.split('_')[0] if '_' in pbn else pbn
# distance = "euklid"


def pop_m(ar):
    return ar[ar != "-"]


def calc_mdos(pbn, pr, alias, distance):
    dist_file = "output/" + pbn + "/" + pr + "_" + alias + "_" + distance + "_dist.csv"
    with open(dist_file, "r") as file:
        lines = file.readlines()
        absolut_distance = float(lines[0].strip())
        len_of_signal = int(lines[1].strip())
    mean_distance_of_signal = absolut_distance * 1.0 / len_of_signal
    return absolut_distance, mean_distance_of_signal


def analyse_path(pbn, pr, alias, distance):
    zeroct = 0
    plusct = 0
    minusct = 0
    maxd = 0
    mind = 0
    maxdist = 0
    mindist = 9999
    list_file = "output/" + pbn + "/" + pr + "_" + alias + "_" + distance + "_list.csv"
    list_df = pd.read_csv(list_file)
    path_ref = list_df["path_ref"].to_numpy()
    path_query = list_df["path_query"].to_numpy()

    ref_x = pop_m(list_df["ref_x"].to_numpy())
    ref_y = pop_m(list_df["ref_y"].to_numpy())
    query_x = pop_m(list_df["query_x"].to_numpy())
    query_y = pop_m(list_df["query_y"].to_numpy())
    distlist = []
    for i in range(len(path_ref)):
        p_x = path_ref[i]
        p_y = path_query[i]
        oh = p_x - p_y
        if oh > 0:
            plusct += 1
            if oh > maxd:
                maxd = oh
        elif oh == 0:
            zeroct += 1
        else:
            minusct += 1
            if oh < mind:
                mind = oh

        dist = -1
        u = [float(ref_x[path_ref[i]]), float(ref_y[path_ref[i]])]
        v = [float(query_x[path_query[i]]), float(query_y[path_query[i]])]
        if distance == "euklid":
            dist = distance_2dim(u, v)
        elif distance == "winkel":
            dist = distance_winkel(u, v)
        elif distance == "winkellog":
            dist = distance_winkel4(u, v)
        distlist.append(dist)
    maxdist = max(distlist)
    mindist = min(distlist)
    med = statistics.median(distlist)

    return med, zeroct, plusct, minusct, maxd, mind, maxdist, mindist


def calc_heatmap(pbn, pr, alias, distance):
    list_file = "output/" + pbn + "/" + pr + "_" + alias + "_" + distance + "_list.csv"

    list_df = pd.read_csv(list_file)
    path_ref = list_df["path_ref"].to_numpy()
    path_query = list_df["path_query"].to_numpy()

    ref_x = pop_m(list_df["ref_x"].to_numpy())
    ref_y = pop_m(list_df["ref_y"].to_numpy())
    query_x = pop_m(list_df["query_x"].to_numpy())
    query_y = pop_m(list_df["query_y"].to_numpy())
    name = "plots/Pathmaps/" + pbn + "_" + alias + "_" + distance + "_pathmap.png"
    pmap = Pathmap(path_ref, path_query, ref_x, ref_y, query_x, query_y, distance, name)
    pmap.heatmap2()


def auswertung(pbnlist, distances, aliases):
    results = []
    header = ["Proband", "IP", "Video", "Distancemeasure", "total_distance", "mean_distance", "median_distance",
              "zero-overhead-counter",
              "ref before query (rbq)",
              "query berfore ref (qbr)", "max rbq", "max qbr", "max distance", "min distance"]
    for pbn in pbnlist:
        pr = pbn.split('_')[0] if '_' in pbn else pbn
        ip = pbn.split('_')[1] if '_' in pbn else 1
        for alias in aliases:
            for dist in distances:
                pbnres = [pr, ip, alias, dist]
                dos, mdos = calc_mdos(pbn, pr, alias, dist)
                pbnres.append(dos)
                pbnres.append(mdos)
                med, zeroct, plusct, minusct, max, min, maxdist, mindist = analyse_path(pbn, pr, alias, dist)
                pbnres.append(med)
                pbnres.append(zeroct)
                pbnres.append(plusct)
                pbnres.append(minusct)
                pbnres.append(max)
                pbnres.append(min)
                pbnres.append(maxdist)
                pbnres.append(mindist)

                results.append(pbnres)
        print("pbn done: "+ pbn)
    return header, results


def write_ausw_zu(header, results):
    name = "output/auswertung1_1-8(o6)_neu"
    inputfile = name + ".csv"
    name2 = "output/auswertung1_1-13(o6)"
    outputfile = name2 + ".csv"
    with open(inputfile, "r", newline='', encoding='utf-8') as file:
        old = file.readlines()
        oldsep = [header]
        for line in old[1:]:
            oldsep.append([a.replace('\"', '') for a in line.split(';')])
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for row in oldsep:
            writer.writerow(row)
        for row in results:
            writer.writerow(row)


def write_ausw(header, results):
    # name = "output/" + pbn + "/" + pbn + "_auswertung1"
    name = "output/auswertung1_1-13(o6)_neu"
    outputfile = name + ".csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(header)
        for row in results:
            writer.writerow(row)


def hg(pbn, pr, alias, distance):
    list_file = "output/" + pbn + "/" + pr + "_" + alias + "_" + distance + "_list.csv"

    list_df = pd.read_csv(list_file)
    path_ref = list_df["path_ref"].to_numpy()
    path_query = list_df["path_query"].to_numpy()

    ref_x = pop_m(list_df["ref_x"].to_numpy())
    ref_y = pop_m(list_df["ref_y"].to_numpy())
    query_x = pop_m(list_df["query_x"].to_numpy())
    query_y = pop_m(list_df["query_y"].to_numpy())

    overhead = [path_ref[i] - path_query[i] for i in range(len(path_ref))]

    if distance == "euklid":
        dist = [distance_2dim([float(ref_x[path_ref[i]]), float(ref_y[path_ref[i]])],
                              [float(query_x[path_query[i]]), float(query_y[path_query[i]])]) for i in
                range(len(path_ref))]
    elif distance == "winkel":
        dist = [distance_winkel([float(ref_x[path_ref[i]]), float(ref_y[path_ref[i]])],
                                [float(query_x[path_query[i]]), float(query_y[path_query[i]])]) for i in
                range(len(path_ref))]
    elif distance == "winkellog":
        dist = [distance_winkel4([float(ref_x[path_ref[i]]), float(ref_y[path_ref[i]])],
                                 [float(query_x[path_query[i]]), float(query_y[path_query[i]])]) for i in
                range(len(path_ref))]
    else:
        raise NotImplementedError
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.subplots_adjust(hspace=0.5)
    ax1.hist(overhead, bins='auto')
    ax2.hist(dist, bins='auto')


if __name__ == "__main__":
    '''
    pbnlist = ["pb1", "pb1_2", "pb2", "pb3", "pb3_2", "pb4", "pb5", "pb5_2", "pb7", "pb7_2", "pb8", "pb9", "pb9_2",
               "pb10", "pb11", "pb11_2", "pb12", "pb13", "pb13_2"]

    distances = ["euklid", "winkel", "winkellog"]

    header, results = auswertung(pbnlist, distances, aliases)
    write_ausw(header, results)
    '''

    pbn = sys.argv[1]
    #pbn = "pb1"
    alias = "BGL1"
    distance = sys.argv[2]
    #distance = "winkellog"
    pr = pbn.split('_')[0] if '_' in pbn else pbn
    calc_heatmap(pbn, pr, alias, distance)
    print("done")

