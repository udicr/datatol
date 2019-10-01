import pandas as pd
import numpy as np
from Pathmap import Pathmap
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
    return mean_distance_of_signal


def calc_heatmap(pbn, pr, alias, distance):
    list_file = "output/" + pbn + "/" + pr + "_" + alias + "_" + distance + "_list.csv"

    list_df = pd.read_csv(list_file)
    path_ref = list_df["path_ref"].to_numpy()
    path_query = list_df["path_query"].to_numpy()

    ref_x = pop_m(list_df["ref_x"].to_numpy())
    ref_y = pop_m(list_df["ref_y"].to_numpy())
    query_x = pop_m(list_df["query_x"].to_numpy())
    query_y = pop_m(list_df["query_y"].to_numpy())
    name = "plots/" + pbn + "/" + pr + "_" + alias + "_" + distance + "_pathmap.png"
    pmap = Pathmap(path_ref, path_query, ref_x, ref_y, query_x, query_y, distance, name)
    pmap.heatmap()





if __name__ == "__main__":
    pbn = sys.argv[1]
    pr = pbn.split('_')[0] if '_' in pbn else pbn
    alias = "Spot1"
    distances = ["euklid", "winkel", "winkellog"]
    for distance in distances:
        calc_heatmap(pbn, pr, alias, distance)
