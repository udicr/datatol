import pandas as pd
import numpy as np
from Pathmap import Pathmap
from multiprocessing.dummy import Pool as ThreadPool
import datetime
import subprocess
import sys
import csv
from distances import *

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


def pop_m(ar):
    return ar[ar != "-"]


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
    ax1.title.set_text("Overhead")
    ax2.hist(dist, bins='auto')
    ax2.title.set_text("Distance")

    name = "plots/Histogramme/" + pbn + "_" + alias + "_" + distance + "_histogramm.png"
    plt.savefig(name)


def pathplot(pbn, pr, alias, distance):
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
    ax1.plot(path_ref, overhead)
    ax1.title.set_text("Overhead")
    ax2.hist(overhead, bins='auto')
    ax2.title.set_text("Histogramm")

    name = "plots/Pathplots/" + pbn + "_" + alias + "_" + distance + "_histogramm.png"
    plt.savefig(name)


if __name__ == "__main__":
    pbn = sys.argv[1]
    alias = sys.argv[2]
    distance = sys.argv[3]
    pr = pbn.split('_')[0] if '_' in pbn else pbn
    hg(pbn, pr, alias, distance)
    pathplot(pbn, pr, alias, distance)
