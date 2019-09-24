from distances import *
import seaborn as sns
from tqdm import tqdm
from matplotlib import pyplot as plt
import pandas as pd
from dtaidistance import dtw_visualisation
from time import time

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
            matrix[self.p_r[i],self.p_q[i]] = 1000
            for k in range(-5,5):
                for l in range(-5,5):
                    try:
                        matrix[self.p_r[i]+k,self.p_q[i]+l] = 1000
                    except IndexError:
                        continue
        return matrix

    def heatmap(self):
        t0 = time()
        m = self.get_matrix()[::-1,:]
        fig = plt.figure(1)
        plt.subplots(figsize = (60,50))
        sns.heatmap(m, xticklabels=1000, yticklabels=1000)
        plt.savefig(self.name)
        t = time() - t0
        print("Generating Distance Matrix and Plotting took "+str(t))


