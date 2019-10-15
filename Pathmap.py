from distances import *
import seaborn as sns
from tqdm import tqdm
from matplotlib import pyplot as plt
import pandas as pd
# from dtaidistance import dtw_visualisation
from time import time
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from itertools import chain


class Pathmap:
    def __init__(self, p_r, p_q, r_x, r_y, q_x, q_y, distance_alias, name, path=""):
        self.p_r = p_r
        self.p_q = p_q
        self.path_len = len(p_r)
        self.r_x = r_x
        self.r_y = r_y
        self.q_x = q_x
        self.q_y = q_y
        self.signal_len = len(r_x)
        self.name = name
        self.path = path
        if distance_alias == "euklid":
            self.distance = distance_2dim
        elif distance_alias == "winkel":
            self.distance = distance_winkel
        elif distance_alias == "winkellog":
            self.distance = distance_winkel4
        else:
            raise NotImplementedError("0 - Euklid, 1 - Winkel, 2 - Winkellog")

    def d(self, i, j):
        u = [float(self.r_x[i]), float(self.r_y[i])]
        v = [float(self.q_x[j]), float(self.q_y[j])]
        return self.distance(u, v)

    def get_matrix(self):
        matrix = np.empty([self.signal_len, self.signal_len])
        for i in tqdm(range(self.signal_len)):
            for j in range(self.signal_len):
                matrix[i, j] = self.d(i, j)
        for i in range(self.path_len):
            matrix[self.p_r[i], self.p_q[i]] = 1000
            for k in range(-10, 10):
                for l in range(-10, 10):
                    try:
                        matrix[self.p_r[i] + k, self.p_q[i] + l] = 1000
                    except IndexError:
                        continue
        return matrix

    def heatmap(self):
        t0 = time()
        m = self.get_matrix()[::-1, :]
        fig = plt.figure(1)
        plt.subplots(figsize=(60, 50))
        sns.heatmap(m, xticklabels=1000, yticklabels=False)
        plt.savefig(self.name)
        plt.clf()
        t = time() - t0
        print("Generating Distance Matrix and Plotting took " + str(t))

    def get_matrix2(self):
        matrix = np.empty([self.signal_len, self.signal_len])
        maxdist = 0
        for i in tqdm(range(self.signal_len)):
            for j in range(max([0, i - 1501]), min([i + 1501, self.signal_len])):
                d = self.d(i, j)
                matrix[i, j] = d
                if d > maxdist:
                    maxdist = d
        path_val = maxdist + 50
        for i in range(self.path_len):
            matrix[self.p_r[i], self.p_q[i]] = path_val
            for k in range(-10, 10):
                for l in range(-10, 10):
                    try:
                        matrix[self.p_r[i] + k, self.p_q[i] + l] = path_val
                    except IndexError:
                        continue

        return matrix

    def get_matrix_adaptiv(self):
        matrix = np.empty([self.signal_len, self.signal_len])
        maxdist = 0
        my_iter = chain(range(-750, -10), range(10, 750))
        my_iter2 = chain(range(-750, -10), range(10, 750))
        for i in tqdm(range(self.path_len)):
            for l in range(2):
                for k in range(10, 750):
                    x = self.p_r[i] - k + l
                    y = self.p_q[i] + k
                    if 0 <= x < self.signal_len and 0 <= y < self.signal_len:
                        d = self.d(x, y)
                        matrix[x, y] = d
                        if d > maxdist:
                            maxdist = d
                    x = self.p_r[i] + k + l
                    y = self.p_q[i] - k
                    if 0 <= x < self.signal_len and 0 <= y < self.signal_len:
                        d = self.d(x, y)
                        matrix[x, y] = d
                        if d > maxdist:
                            maxdist = d

        path_val = maxdist + 50
        for i in range(self.path_len):
            matrix[self.p_r[i], self.p_q[i]] = path_val
            for k in range(-10, 10):
                for l in range(-10, 10):
                    try:
                        matrix[self.p_r[i] + k, self.p_q[i] + l] = path_val
                    except IndexError:
                        continue

        return matrix

    def heatmap2(self):
        fontsize = 30
        t0 = time()
        m = self.get_matrix_adaptiv()       #[::-1, :]
        # mask = np.array(
        #   [[False if abs(i - (self.signal_len-j)) <= 1500 else True for i in range(self.signal_len)] for j in range(self.signal_len)])

        fig, ax = plt.subplots(figsize=(60, 50))
        c = ax.imshow(m, cmap="viridis")
        cb = fig.colorbar(c, ax=ax, fraction=0.046, pad=0.04)
        plt.gca().invert_yaxis()
        #cb.set_label(label='distance')
        ax.tick_params(labelsize=fontsize)
        cb.ax.tick_params(labelsize=fontsize)
        plt.savefig(self.name)
        plt.clf()
        t = time() - t0
        print("Generating Distance Matrix and Plotting took " + str(t))
