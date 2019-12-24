from numpy import *
import scipy as sp
from pandas import *
import pandas as pd
import pyreadr
from fastdtw import fastdtw
from dtaidistance import dtw_ndim
from dtaidistance import dtw as dtaidtw
from dtaidistance import dtw_visualisation as dtwvis
from dtaidistance import dtw_ndim_visualisation as ndtwvis
# from dtw import accelerated_dtw, dtw
from dtw import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from time import time
import csv
from distances import *
import os
from multiprocessing.dummy import Pool as ThreadPool
import datetime
import sys
from cdtw import pydtw
import gc

plotting = 0
'''
    "BGL1",
    "BGL2",
    "BGL3",
    "BGL4",
    "BGL5",
    "BGL6",
    "BGL7",
    "BGL8",
'''
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


def check_datadir():
    try:
        os.mkdir('./data/')
        print("Error: keine Daten vorhanden")
        raise FileNotFoundError
    except OSError as e:
        pass


def check_plottingdir():
    try:
        os.mkdir('./plots/')
        print("Ordner fuer Output-Plots")
    except OSError as e:
        pass


def check_plottingdir_pbn(pbn):
    try:
        pb_no = int(pbn[2:])
        if pb_no % 2 == 1:
            os.mkdir('./plots/' + pbn + '_2/')
        os.mkdir('./plots/' + pbn + '/')
        print("Erstelle Ordner fuer Output-Plots")
    except OSError as e:
        pass


def check_outputdir():
    try:
        os.mkdir('./output/')
        print("Erstelle Ordner fuer Output")
    except OSError as e:
        pass


def check_outputdir_pbn(pbn):
    try:
        pb_no = int(pbn[2:])
        if pb_no % 2 == 1:
            os.mkdir('./output/' + pbn + '_2/')
        os.mkdir('./output/' + pbn + '/')

        print("Erstelle Ordner fuer Output")
    except OSError as e:
        pass


def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]


def blink_correct(data):
    """ Interpolates between Fixations (all Saccades and Blinks)
    :param data: ndarray
    :return: data: ndarray
    """
    for c in data:
        if c[0] == c[1] == 0:
            c[0] = c[1] = np.nan
        try:
            c[0] = float(c[0])
        except ValueError:
            c[0] = float(str(c[0]).replace(',', '.'))
        try:
            c[1] = float(c[1])
        except ValueError:
            c[1] = float(str(c[1]).replace(',', '.'))

    datax = np.array(data[:, 0], dtype=np.float64)
    datay = np.array(data[:, 1], dtype=np.float64)

    nans, tmp = nan_helper(datax)
    datax[nans] = np.interp(tmp(nans), tmp(~nans), datax[~nans])
    nans, tmp = nan_helper(datay)
    datay[nans] = np.interp(tmp(nans), tmp(~nans), datay[~nans])
    data_out = np.column_stack((datax, datay))
    return data_out


def plot_getrennt(r2D, q2D, path, factor=50, file="plot.png"):
    ''' Compare two 3D-Plots if ref and query with Dtw-Connection-Lines
    :param r2D:
    :param q2D:
    :param path:
    :param factor:
    :param file:
    :return:
    '''
    ref1D = r2D[:, 0]
    ref1D2 = r2D[:, 1]
    query1D = q2D[:, 0]
    query1D2 = q2D[:, 1]
    path = path[::factor]

    fig = plt.figure()  # vgl https://stackoverflow.com/questions/19473902/connectionpatch-for-3d-subplots

    # a background axis to draw lines on
    ax0 = plt.axes([0., 0., 1., 1.])
    ax0.set_xlim(0, 1)
    ax0.set_ylim(0, 1)

    # use these to know how to transform the screen coords
    dpi = ax0.figure.get_dpi()
    height = ax0.figure.get_figheight() * dpi
    width = ax0.figure.get_figwidth() * dpi

    # query
    ax1 = fig.add_subplot(2, 1, 1, projection='3d')

    plt.plot(range(len(query1D)), query1D, query1D2, 'r', label="query")
    ax1.view_init(-165, -85)
    # ax1.set_zlim((max(max(query1D2), max(ref1D2))+50, min(min(query1D2), min(ref1D2))-50))
    ax1.set_zlim((min(min(query1D2), min(ref1D2)) - 50, max(max(query1D2), max(ref1D2)) + 50))
    ax1.set_ylim((min(min(query1D), min(ref1D)) - 50, max(max(query1D), max(ref1D)) + 50))
    plt.legend()

    ax1.set_xlabel('$t$')
    ax1.set_ylabel('$x$')
    ax1.set_zlabel('$y$')

    # ref
    ax2 = fig.add_subplot(2, 1, 2, projection='3d')
    plt.plot(range(len(ref1D)), ref1D, ref1D2, 'b', label="ref")
    ax2.view_init(-165, -85)
    # ax2.set_zlim((max(max(query1D2), max(ref1D2))+50, min(min(query1D2), min(ref1D2))-50))
    ax2.set_zlim((min(min(query1D2), min(ref1D2)) - 50, max(max(query1D2), max(ref1D2)) + 50))
    ax2.set_ylim((min(min(query1D), min(ref1D)) - 50, max(max(query1D), max(ref1D)) + 50))
    plt.legend()

    ax2.set_xlabel('$t$')
    ax2.set_ylabel('$x$')
    ax2.set_zlabel('$y$')

    # connection lines
    for tupel in path:
        i = tupel[0]
        j = tupel[1]
        c1, c2, c3 = [i, j], [ref1D[i], query1D[j]], [ref1D2[i], query1D2[j]]

        # first point of interest
        p1 = ([c1[1]], [c2[1]], [c3[1]])
        ax1.plot(p1[0], p1[1], p1[2], 'g')
        x1, y1, _ = proj3d.proj_transform(p1[0], p1[1], p1[2], ax1.get_proj())
        [x1, y1] = ax1.transData.transform((x1[0], y1[0]))  # convert 2d space to screen space
        # put them in screen space relative to ax0
        x1 = x1 / width
        y1 = y1 / height

        # another point of interest
        p2 = ([c1[0]], [c2[0]], [c3[0]])
        ax2.plot(p2[0], p2[1], p2[2], 'g')
        x2, y2, _ = proj3d.proj_transform(p2[0], p2[1], p2[2], ax2.get_proj())
        [x2, y2] = ax2.transData.transform((x2[0], y2[0]))  # convert 2d space to screen space
        x2 = x2 / width
        y2 = y2 / height

        # set all these guys to invisible (needed?, smartest way?)
        for item in [fig, ax1, ax2]:
            item.patch.set_visible(False)

        # plot line between subplots
        transFigure = fig.transFigure.inverted()
        coord1 = transFigure.transform(ax0.transData.transform([x1, y1]))
        coord2 = transFigure.transform(ax0.transData.transform([x2, y2]))
        fig.lines = ax0.plot((coord1[0], coord2[0]), (coord1[1], coord2[1]), color='lightgreen',
                             transform=fig.transFigure, linewidth=0.7)  # , linestyle='dashed'

        # plt.plot(c1, c2, c3,'g', label="connect",linewidth=0.5)   stack all in one subplot and draw

    plt.savefig(file)
    plt.close(fig)


def plot_zusammen(r2D, q2D, path, factor=20, file="plot.png"):
    '''compares 2 3D signals(ref and query) in one Plot with DTW Connection Lines
    :param r2D:
    :param q2D:
    :param path:
    :param factor:
    :param file:
    :return:
    '''
    ref1D = r2D[:, 0]
    ref1D2 = r2D[:, 1]
    query1D = q2D[:, 0]
    query1D2 = q2D[:, 1]
    path = path[::factor]

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1, projection='3d')
    ax1.view_init(-172, -88)
    plt.plot(range(len(query1D)), query1D, query1D2, label="query")
    plt.plot(range(len(ref1D)), ref1D, ref1D2, label="ref")
    plt.legend()
    # ax1.set_zlim((max(max(query1D2), max(ref1D2))+50, min(min(query1D2), min(ref1D2))-50))
    ax1.set_ylim((min(min(query1D), min(ref1D)) - 50, max(max(query1D), max(ref1D)) + 50))
    ax1.set_xlabel('$t$')
    ax1.set_ylabel('$x$')
    ax1.set_zlabel('$y$')
    # connection lines
    for tupel in path:
        i = tupel[0]
        j = tupel[1]
        c1, c2, c3 = [i, j], [ref1D[i], query1D[j]], [ref1D2[i], query1D2[j]]
        plt.plot(c1, c2, c3, 'g', label="connect", linewidth=0.5)
    # plt.show()
    plt.savefig(file)
    plt.close(fig)


def save_old(path, distance, path2, distance2, n, name="test"):
    '''
    saves path,distance,path2,distance2 and n in name.csv
    :param path:
    :param distance:
    :param path2:
    :param distance2:
    :param n:
    :param name:
    :return:
    '''
    outputfile = name + ".csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["Path", "Path", "Distance", "Path2", "Path2", "Distance2", "n"])
        writer.writerow([path[0][0], path[0][1], distance, path2[0][0], path2[0][1], distance2, n])
        print(len(path))
        print(len(path2))

        for i in range(1, min([len(path), len(path2)])):
            writer.writerow([path[i][0], path[i][1], "", path2[i][0], path2[i][1], "", ""])
        if len(path) < len(path2):
            for i in range(len(path), len(path2)):
                writer.writerow(["", "", "", path2[i][0], path2[i][1], "", ""])
        if len(path) > len(path2):
            writer.writerow([path[i][0], path[i][1], "", "", "", "", ""])


def save(path, ref, query, n, distance, pdistance, prob="00", alias="alias", dist=0, ip=1):
    if dist == 0:
        name = prob + "_" + alias + "_euklid"
    elif dist == 1:
        name = prob + "_" + alias + "_winkel"
    elif dist == 2:
        name = prob + "_" + alias + "_winkellog"
    else:
        raise NotImplementedError("0 - Euklid, 1 - Winkel, 2 - Winkellog")
    if ip == 1:
        outputfile1 = "output/" + prob + "/" + name + "_dist.csv"
        outputfile2 = "output/" + prob + "/" + name + "_list.csv"
    else:
        outputfile1 = "output/" + prob + "_" + str(ip) + "/" + name + "_dist.csv"
        outputfile2 = "output/" + prob + "_" + str(ip) + "/" + name + "_list.csv"
    with open(outputfile1, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([distance])
        writer.writerow([n])
    header = ["path_ref", "path_query", "path_distance", "ref_x", "ref_y", "query_x", "query_y"]
    with open(outputfile2, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)
        for i in range(n):
            writer.writerow([path[i][0], path[i][1], pdistance[i], ref[i, 0], ref[i, 1], query[i, 0], query[i, 1]])
        for i in range(n, len(path)):
            writer.writerow([path[i][0], path[i][1], pdistance[i], "-", "-", "-", "-"])


def do_whole_pb(prob="pb1"):
    pb_no = int(prob[2:])
    print(pb_no)
    print("Reading Data ...")
    rda = pyreadr.read_r(prob + ".Rda")
    df = rda["m.df_pb"]
    pb_no = int(prob[2:])
    print(pb_no)
    if pb_no % 2 == 0:
        mode = "slow"
    else:
        mode = "fast"

    for alias in aliases:
        if mode == "slow":
            cut = df[df.video == alias]
            do_video(cut, prob, alias)
        elif mode == "fast":
            cut = df[df.video == alias]
            cut_1 = cut[cut.IP_INDEX == 1]
            cut_2 = cut[cut.IP_INDEX == 2]
            print("Doing first block")
            do_video(cut_1, prob, alias, 1)
            print("Doing second block")
            do_video(cut_2, prob, alias, 2)
        else:
            raise (KeyError)


def do_pb_outside(prob="pb1", alias="Spot1"):
    pb_no = int(prob[2:])
    print(pb_no)
    print(alias)
    print("Reading Data ...")
    rda = pyreadr.read_r(prob + ".Rda")
    df = rda["m.df_pb"]

    if pb_no % 2 == 0:
        mode = "slow"
    else:
        mode = "fast"
    if mode == "slow":
        cut = df[df.video == alias]
        do_video(cut, prob, alias)
    elif mode == "fast":
        cut = df[df.video == alias]
        cut_1 = cut[cut.IP_INDEX == 1]
        cut_2 = cut[cut.IP_INDEX == 2]
        print("Doing first block")
        do_video(cut_1, prob, alias, 1)
        print("Doing second block")
        do_video(cut_2, prob, alias, 2)
    else:
        raise (KeyError)


def get_path_distances(p, r, q, distance):
    d = [distance([r[p[i][0], 0], r[p[i][0], 1]], v=[q[p[i][1], 0], q[p[i][1], 1]]) for i in range(len(p))]
    return d


def do_video(cut, prob, alias, ip=1):
    pb = prob if ip == 1 else prob + "_" + str(ip)
    dtw_pack = "dtw"
    distances = [distance_2dim, distance_winkel, distance_winkel4]
    for i in range(3):
        ref = cut[['x_coord', 'y_coord']].to_numpy(copy=True)
        query = cut[['CURRENT_FIX_X', 'CURRENT_FIX_Y']].to_numpy(copy=True)

        ref2D = blink_correct(ref)
        query2D = blink_correct(query)
        n = len(ref2D[:, 0])

        print("Doing DTW ...")

        if dtw_pack == "fastdtw":
            distance, path = fastdtw(ref2D, query2D, dist=distances[i])
        elif dtw_pack == "dtaidistance":
            distance, paths = dtw_ndim.warping_paths(ref2D, query2D, window=500)
            path = dtaidtw.best_path(paths)
            # ndtwvis.plot_warpingpaths(ref2D, query2D, paths, path, filename="test1.jpg")
        elif dtw_pack == "dtw":
            if i == 0:
                name = pb + "_" + alias + "_euklid"
            elif i == 1:
                name = pb + "_" + alias + "_winkel"
            elif i == 2:
                name = pb + "_" + alias + "_winkellog"
            else:
                raise KeyError
            if not_done_yet(name):
                distance, cost_matrix, acc_cost_matrix, path = dtw(ref2D, query2D, distances[i], w=500)
                np.save("matrices/" + name + "_cost_matrix", cost_matrix)
                #np.save("matrices/" + name + "_acc_cost_matrix", acc_cost_matrix)
                np.save("matrices/" + name + "path", path)
                print("Generating Path")
                path = np.column_stack(path)
            else:
                print("Skipped already existing Trial: " + name)
                continue
        elif dtw_pack == "cdtw":
            d = pydtw.dtw(ref2D, query2D, pydtw.Settings(window='palival', param=2.0, compute_path=True))
            distance = d.get_dist()
            path = d.get_path()
            raise NotImplementedError  # doesnt work yet
        else:
            raise ModuleNotFoundError
        print("Calculating Path Distances")
        path_distances = get_path_distances(path, ref2D, query2D, distances[i])

        print("Saving Results ...")
        save(path, ref2D, query2D, n, distance, path_distances,
             prob=prob, alias=alias, dist=i, ip=ip)
        gc.collect()


def not_done_yet(name):
    # return os.path.isfile("matrices/" + name + "_cost_matrix")
    return True


def make_plots(pbn, video="all"):  # for fast ones u have to call make_plots("pb1") AND make_plots("pb1_2")
    pr = pbn.split('_')[0] if "_" in pbn else pbn
    if video != "all":
        csvfile1 = "output/" + pbn + "/" + pr + "_" + video + "_euklid_list.csv"
        csvfile2 = "output/" + pbn + "/" + pr + "_" + video + "_winkel_list.csv"
        csvfile3 = "output/" + pbn + "/" + pr + "_" + video + "_winkellog_list.csv"
        csvfiles = [csvfile1, csvfile2, csvfile3]
    else:
        csvfiles = []
        csvfiles += ["output/" + pbn + "/" + pr + "_" + alias + "_euklid_list.csv" for alias in aliases]
        csvfiles += ["output/" + pbn + "/" + pr + "_" + alias + "_winkel_list.csv" for alias in aliases]
        csvfiles += ["output/" + pbn + "/" + pr + "_" + alias + "_winkellog_list.csv" for alias in aliases]
        # print(csvfiles)
    for csvfile in csvfiles:
        df = pd.read_csv(csvfile)

        path = df[['path_ref', 'path_query']].to_numpy(copy=True)

        n = path[-1, 1]
        mask = df.index <= n
        sf = df[mask]

        ref = sf[['ref_x', 'ref_y']].to_numpy(copy=True).astype(float)

        query = sf[['query_x', 'query_y']].to_numpy(copy=True).astype(float)

        name = csvfile.split('.')[0].split('/')[2]
        name1 = "plots/" + pbn + "/" + name + "_1.png"
        name2 = "plots/" + pbn + "/" + name + "_2.png"
        plot_getrennt(ref, query, path, factor=50, file=name1)
        plot_zusammen(ref, query, path, factor=50, file=name2)


def main(pb):
    check_datadir()
    check_plottingdir()
    check_outputdir()
    check_outputdir_pbn(pb)
    check_plottingdir_pbn(pb)
    t0 = time()
    do_whole_pb(pb)
    print("PB " + pb + " done:")
    print(time() - t0)


def main_parallel(pb, al):
    check_datadir()
    check_plottingdir()
    check_outputdir()
    check_outputdir_pbn(pb)
    check_plottingdir_pbn(pb)
    t0 = time()
    do_pb_outside(pb, al)
    print("PB " + pb + " Alias " + al + " done:")
    print(time() - t0)


def plot_multi():
    pool = ThreadPool(4)
    pbns = ["pb1", "pb2", "pb3", "pb4"]
    check_plottingdir()
    for pb in pbns:
        check_plottingdir_pbn(pb)
    results = pool.map(make_plots, pbns)
    with open("DTW_log_plotting.txt", "a") as file:
        file.write("Log_from_DTW:PLOTTING at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")


if __name__ == "__main__":
    parallelmode = 1
    if parallelmode == 0:
        datamode = True
        plotmode = False
        if len(sys.argv) > 2:
            datamode = True
            plotmode = True
        if datamode:
            if len(sys.argv) < 2:
                print("Argument <PBN> required")
            else:
                pbn = sys.argv[1]
                main(pbn)
        if plotmode:
            if len(sys.argv) < 2:
                print("Argument <PBN> required")
            else:
                pbn = sys.argv[1]
                make_plots(pbn)
    elif parallelmode == 1:
        if len(sys.argv) < 3:
            print("Arguments <PBN> <ALIAS> required")
        else:
            pbn = sys.argv[1]
            al = sys.argv[2]
            main_parallel(pbn, al)
            # make_plots(pbn)
