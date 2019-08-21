from numpy import *
import scipy as sp
from pandas import *
import pandas as pd
import pyreadr
from fastdtw import fastdtw
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
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

plotting = 0
aliases = ["Spot1",
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
        print("Erstelle Ordner für Output-Plots")
    except OSError as e:
        pass


def check_plottingdir_pbn(pbn):
    try:
        os.mkdir('./plots/' + pbn + '/')
        print("Erstelle Ordner für Output-Plots")
    except OSError as e:
        pass


def check_outputdir():
    try:
        os.mkdir('./output/')
        print("Erstelle Ordner für Output")
    except OSError as e:
        pass


def check_outputdir_pbn(pbn):
    try:
        os.mkdir('./output/' + pbn + '/')
        print("Erstelle Ordner für Output")
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
    datax = data[:, 0]
    datay = data[:, 1]
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


def save(path, ref, query, n, distance, prob="00", alias="alias", dist=0):

    if dist == 0:
        name = prob + "_" + alias + "_euklid"
    elif dist == 1:
        name = prob + "_" + alias + "_winkel"
    elif dist == 2:
        name = prob + "_" + alias + "_winkellog"
    else:
        raise ValueError("0 - Euklid, 1 - Winkel, 2 - Winkellog")
    outputfile1 = "output/" + prob + "/" + name + "_dist.csv"
    outputfile2 = "output/" + prob + "/" + name + "_list.csv"
    with open(outputfile1, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([distance])
        writer.writerow([n])
    header = ["path_ref", "path_query", "ref_x", "ref_y", "query_x", "query_y"]
    with open(outputfile2, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)
        for i in range(n):
            writer.writerow([path[i][0], path[i][1], ref[i, 0], ref[i, 1], query[i, 0], query[i, 1]])
        for i in range(n, len(path)):
            writer.writerow([path[i][0], path[i][1], "-", "-", "-", "-"])


def do_whole_pb(prob="pb1"):
    print("Reading Data ...")
    rda = pyreadr.read_r(prob + ".Rda")
    df = rda["m.df_pb"]

    for alias in aliases:
        cut = df[df.video == alias]
        do_video(cut, prob, alias)


def do_video(cut, prob, alias):
    distances = [distance_2dim, distance_winkel, distance_winkel4]
    for i in range(3):
        ref = cut[['x_coord', 'y_coord']].to_numpy(copy=True)
        query = cut[['CURRENT_FIX_X', 'CURRENT_FIX_Y']].to_numpy(copy=True)

        ref2D = blink_correct(ref)
        query2D = blink_correct(query)
        n = len(ref2D[:, 0])

        print("Doing DTW ...")

        distance, path = fastdtw(ref2D, query2D, dist=distances[i])

        print("Saving Results ...")
        save(path, ref2D, query2D, n, distance, prob=prob, alias=alias, dist=i)


def make_plots(pbn, video="all"):
    if video != "all":
        csvfile1 = "output/" + pbn + "/" + pbn + "_" + video + "_euklid_list.csv"
        csvfile2 = "output/" + pbn + "/" + pbn + "_" + video + "_winkel_list.csv"
        csvfile3 = "output/" + pbn + "/" + pbn + "_" + video + "_winkellog_list.csv"
        csvfiles = [csvfile1, csvfile2, csvfile3]
    else:
        csvfiles = []
        csvfiles += ["output/" + pbn + "/" + pbn + "_" + alias + "_euklid_list.csv" for alias in aliases]
        csvfiles += ["output/" + pbn + "/" + pbn + "_" + alias + "_winkel_list.csv" for alias in aliases]
        csvfiles += ["output/" + pbn + "/" + pbn + "_" + alias + "_winkellog_list.csv" for alias in aliases]
    for csvfile in csvfiles:
        df = pd.read_csv(csvfile)

        path = df[['path_ref', 'path_query']].to_numpy(copy=True)

        n = path[-1, 1]
        mask = df.index <= n
        sf = df[mask]

        ref = sf[['ref_x', 'ref_y']].to_numpy(copy=True).astype(float)

        query = sf[['query_x', 'query_y']].to_numpy(copy=True).astype(float)

        name = csvfile.split('.')[0].split('/')[1]
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
    print("PB "+pb+" done:")
    print(time() - t0)


def main_multi():
    pool = ThreadPool(4)
    pbns = ["pb1", "pb2", "pb3", "pb4"]
    results = pool.map(main, pbns)
    with open("DTW_log.txt", "a") as file:
        file.write("Log_from_DTW:DynTimeWarp at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")


def plot_multi():
    pool = ThreadPool(4)
    pbns = ["pb1", "pb2", "pb3", "pb4"]
    results = pool.map(make_plots, pbns)
    with open("DTW_log_plotting.txt", "a") as file:
        file.write("Log_from_DTW:PLOTTING at " + datetime.datetime.now().strftime("%c"))
        for res in results:
            for r in res:
                file.write(r + "\n")


if __name__ == "__main__":
    main_multi()
