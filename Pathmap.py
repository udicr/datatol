from distances import *


class Pathmap:
    def __init__(self, p_r, p_q, r_x, r_y, q_x, q_y, distance_alias, name, path=""):
        self.p_r = p_r
        self.p_q = p_q
        self.r_x = r_x
        self.r_y = r_y
        self.q_x = q_x
        self.q_y = q_y
        self.name = name
        self.path = path
        if distance_alias == "euklid": self.distance = distance_2dim
        elif distance_alias == "winkel": self.distance = distance_winkel
        elif distance_alias == "winkellog": self.distance = distance_winkel4
        else: raise NotImplementedError("0 - Euklid, 1 - Winkel, 2 - Winkellog")

    def d(self, i, j):
        u = [self.r_x[i], self.r_y[i]]
        v = [self.q_x[j], self.q_y[j]]
        return self.distance(u, v)

    def save(self):
        pass
