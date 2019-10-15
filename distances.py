import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib

M = [960,540]
def distance_2dim(u, v):
    """
    :param u: [u[0],u[1]] point in R^2
    :param v: [v[0],v[1]] point in R^2
    :return: float dist the distance between the two points
    """
    return float(abs(np.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2)))


def distance_winkel(u, v):
    """
    :param u: [u[0],u[1]] point in R^2
    :param v: [v[0],v[1]] point in R^2
    :return: float in [0,180] angle between the two vectors 0 = (960,540), tmp_u , tmp_v vectors
    """
    m = [960, 540]
    tmp_u = [u[0] - m[0], u[1] - m[1]]
    tmp_v = [v[0] - m[0], v[1] - m[1]]
    if tmp_u[0] == tmp_v[0] == tmp_u[1] == tmp_v[1] == 0:
        return 0
    c = np.dot(tmp_u, tmp_v) / np.linalg.norm(tmp_u) / np.linalg.norm(tmp_v)
    t = np.arccos(np.clip(c, -1, 1)) / np.pi * 180
    return t


def distance_winkel2(u, v):
    """
    :param u: [u[0],u[1]] point in R^2
    :param v: [v[0],v[1]] point in R^2
    :return: float in [0,180] angle between the two vectors 0 = (960,540) corrected by norm of vectors
    """
    m = [960, 540]
    tmp_u = [u[0] - m[0], u[1] - m[1]]
    tmp_v = [v[0] - m[0], v[1] - m[1]]
    t = distance_winkel(u, v)
    if tmp_u[0] == tmp_u[1] == 0 or tmp_v[0] == tmp_v[1] == 0:
        return 0

    n = float(abs(np.sqrt((tmp_u[0] - tmp_v[0]) ** 2 + (tmp_u[1] - tmp_v[1]) ** 2)))
    return 0.5 * np.sqrt(t ** 2 + 3 * n ** 2)


def distance_winkel3(u, v):
    """
    :param u: [u[0],u[1]] point in R^2
    :param v: [v[0],v[1]] point in R^2
    :return: float in [0,180] angle between the two vectors 0 = (960,540) corrected exponential
    """
    m = [960, 540]
    tmp_u = [u[0] - m[0], u[1] - m[1]]
    tmp_v = [v[0] - m[0], v[1] - m[1]]
    t = distance_winkel(u, v)
    if tmp_u[0] == tmp_u[1] == 0 or tmp_v[0] == tmp_v[1] == 0:
        return 0
    a = np.sqrt(tmp_u[0] ** 2 + tmp_u[1] ** 2)
    b = np.sqrt(tmp_v[0] ** 2 + tmp_v[1] ** 2)
    #func_ab_old = np.sqrt(a ** 2 + b ** 2) / (a / b + b / a)
    func_ab = max([a,b])
    fn = 1 - np.exp(-0.02 * func_ab)
    return fn * t


def distance_winkel4(u, v):
    """
    :param u: [u[0],u[1]] point in R^2
    :param v: [v[0],v[1]] point in R^2
    :return: float in [0,180] angle between the two vectors 0 = (960,540) corrected logarithmic
    """
    m = [960, 540]
    tmp_u = [u[0] - m[0], u[1] - m[1]]
    tmp_v = [v[0] - m[0], v[1] - m[1]]
    t = distance_winkel(u, v)
    if tmp_u[0] == tmp_u[1] == 0 or tmp_v[0] == tmp_v[1] == 0:
        return 0
    #n = float(abs(np.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2)))
    a = np.sqrt(tmp_u[0] ** 2 + tmp_u[1] ** 2)
    b = np.sqrt(tmp_v[0] ** 2 + tmp_v[1] ** 2)
    #func_ab_old = np.sqrt(a ** 2 + b ** 2) / (a / b + b / a)
    func_ab = max([a,b])
    a_1 = 999
    breite = 50
    a_2 = np.log(110001)/breite
    fax = 0.1
    p = 40 - 50*0.75
    #beta = max([p  - 1/a_2 * np.log(a_1 / (1 - fax)) , 0])
    #beta = (np.log((1-fax)/(a_1*fax))+a_2*p)/a_2
    beta = p + 1/a_2 * np.log((1-fax)/0.1*a_1)
    fn = 1 / (1 + a_1 * np.exp(-a_2
                               * (func_ab - beta)
                                  ))
    return fn*t


def test_distances():
    fig = plt.figure()
    max_norm = np.sqrt(960 ** 2 + 540 ** 2)

    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960, 540 + i * 0.5] for i in range(31*12)]
    m = [960, 540]
    outputfile = "distancetest_90deg.csv"
    d = []
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    # ax2 = [t[0] for t in d]
    plt.subplot(221)
    # plt.plot(ax, [t[0] for t in d], label="Euklidian")
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("90 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    d = []
    u_i = []
    v_i = []
    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960 - i * 1, 540] for i in range(31*12)]
    outputfile = "distancetest_180deg.csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    plt.subplot(222)
    # ax2 = [t[0] for t in d]
    #ax2 = [i * 32 for i in range(0, 31)]
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("180 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    d = []
    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960 + i * 1, 540 + i * 1] for i in range(31*12)]
    outputfile = "distancetest_45deg.csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    plt.subplot(223)
    # ax2 = [t[0] for t in d]
    #ax2 = [i * 32 for i in range(0, 31)]
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("45 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    d = []
    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960 - i * 1, 540 + i * 1] for i in range(31*12)]
    outputfile = "distancetest_135deg.csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    plt.subplot(224)
    # ax2 = [t[0] for t in d]
    #ax2 = [i * 32 for i in range(0, 31)]
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("135 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def test_distances2():
    fig = plt.figure()
    max_norm = np.sqrt(960 ** 2 + 540 ** 2)

    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960 + i * 1, 540 + i * 1 * np.tan(np.deg2rad(60))] for i in range(31*12)]
    m = [960, 540]
    outputfile = "distancetest_60deg.csv"
    d = []
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    # ax = [i for i in range(0,31)]
    #ax2 = [t[0] for t in d]
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    plt.subplot(221)
    # plt.plot(ax, [t[0] for t in d], label="Euklidian")
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("60 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    d = []
    u_i = []
    v_i = []
    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960 + i * 1, 540 + i * 12 * np.tan(np.deg2rad(10))] for i in range(31*12)]
    outputfile = "distancetest_10deg.csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    plt.subplot(222)
    #ax2 = [t[0] for t in d]
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("10 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    d = []
    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960 + i * 1, 540 + i * 1 * np.tan(np.deg2rad(30))] for i in range(31*12)]
    outputfile = "distancetest_30deg.csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    plt.subplot(223)
    #ax2 = [t[0] for t in d]
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("30 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    d = []
    u_i = [[960 + i * 1, 540] for i in range(31*12)]
    v_i = [[960 - i * 1, 540 + i * 1 * np.tan(np.deg2rad(60))] for i in range(31*12)]
    outputfile = "distancetest_120deg.csv"
    with open(outputfile, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["u_0", "u_1", "v_0", "v_1", "Euklid", "Winkel", "Winkel+", "Winkelsk", "Winkellog"])

        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])
            inh = [u_i[i][0],
                   u_i[i][1],
                   v_i[i][0],
                   v_i[i][1],
                   d1,
                   d2,
                   d3,
                   d4,
                   d5
                   ]

            writer.writerow(inh)
    plt.subplot(224)
    #ax2 = [t[0] for t in d]
    ax2 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31*12)]
    plt.plot(ax2, [t[1] for t in d], label="Winkel")
    # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
    plt.plot(ax2, [t[3] for t in d], label="Winkel*")
    plt.plot(ax2, [t[4] for t in d], label="Winkellog")
    plt.title("120 Grad")
    plt.xlabel("Max Länge u,v (euklidisch)")
    plt.ylabel("Winkel")
    plt.legend()

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def test_distances3():
    N = 100
    '''
    
    fps = 5
    frn = 50
    x = np.linspace(0, 1920, N)
    y = np.linspace(0, 1080, N)

    xx, yy = np.meshgrid(x, y)

    Z = np.array(np.zeros([N,N,50]))
    for k in range(1, frn):
        u = [960 + k * 10, 540]
        for i in range(N):
            for j in range(N):
                Z[i, j, k] = distance_winkel(u, [x[i], y[j]])
                if Z[i, j, k] is np.nan:
                    Z[i, j, k] = 0


    fig = plt.figure()

    def update_plot(frame_number, zarray, plot):
        plot[0].remove()
        plot[0] = ax.plot_surface(xx, yy, Z[:,:,frame_number], rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')

    ax = fig.add_subplot(1, 1, 1, projection='3d')
    plot = [ax.plot_surface(xx, yy, Z[:,:,0], rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')]
    ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(Z, plot), interval=1000 / fps)

    fn = 'plot_surface_animation_funcanimation'
    ani.save(fn + '.mp4', writer='ffmpeg', fps=fps)

    '''
    for o in range(11):
        fig = plt.figure()
        Z1 = np.array(np.zeros([N, N]))
        Z2 = np.array(np.zeros([N, N]))
        Z3 = np.array(np.zeros([N, N]))
        x = np.linspace(0, 1920, N)
        y = np.linspace(0, 1080, N)
        u = [960, 545 + 10 * o]

        xx, yy = np.meshgrid(x, y)
        for i in range(100):
            for j in range(100):
                Z1[i, j] = distance_winkel(u, [x[i], y[j]])

        ax = fig.add_subplot(2, 2, 1, projection='3d')
        ax.plot_surface(xx, yy, Z1, rstride=1, cstride=1,
                        cmap='viridis', edgecolor='none');
        ax.quiver(960, 540, 0, 5 + 100 * o, 0, 0)
        ax.view_init(25, 20)
        ax.set_zlim(0, 180)

        for i in range(100):
            for j in range(100):
                Z2[i, j] = distance_winkel3(u, [x[i], y[j]])
        ax2 = fig.add_subplot(2, 2, 3, projection='3d')
        ax2.plot_surface(xx, yy, Z2, rstride=1, cstride=1,
                         cmap='viridis', edgecolor='none');
        ax2.quiver(960, 540, 0, 5 + 100 * o, 0, 0)
        ax2.view_init(25, 20)
        ax2.set_zlim(0, 180)

        for i in range(100):
            for j in range(100):
                Z3[i, j] = distance_winkel4(u, [x[i], y[j]])
        ax3 = fig.add_subplot(2, 2, 4, projection='3d')
        ax3.plot_surface(xx, yy, Z3, rstride=1, cstride=1,
                         cmap='viridis', edgecolor='none');
        ax3.quiver(960, 540, 0, 5 + 100 * o, 0, 0)
        ax3.view_init(25, 20)
        ax3.set_zlim(0, 180)

        u_i = [[960 + i * 32, 540] for i in range(31)]
        v_i = [[960 - i * 32, 540] for i in range(31)]
        d = []
        for i in range(len(u_i)):
            d1 = distance_2dim(u_i[i], v_i[i])
            d2 = distance_winkel(u_i[i], v_i[i])
            d3 = distance_winkel2(u_i[i], v_i[i])
            d4 = distance_winkel3(u_i[i], v_i[i])
            d5 = distance_winkel4(u_i[i], v_i[i])
            d.append([d1, d2, d3, d4, d5])

        plt.subplot(222)
        # ax2 = [t[0] for t in d]
        m = [960,540]
        ax4 = [max([distance_2dim(u_i[j],m),distance_2dim(v_i[j],m)]) for j in range(31)]
        plt.plot(ax4, [t[1] for t in d], label="Winkel")
        # plt.plot(ax2, [t[2] for t in d], label="Winkel+")
        plt.plot(ax4, [t[3] for t in d], label="Winkel*")
        plt.plot(ax4, [t[4] for t in d], label="Winkellog")
        plt.title("180 Grad")
        plt.xlabel("Max Länge u,v (euklidisch)")
        plt.ylabel("Winkel")
        plt.legend()
        plt.show()
        #plt.savefig("Test3_"+str(o)+".png")


if __name__ == "__main__":
    test_distances()
    test_distances2()
    test_distances3()
    '''
    Z1,Z2,Z3 = test_distances3()
    l1 = []
    for zl in Z1:
        for z in zl:
            if z<50:
                l1.append(z)
    l2 = []
    for zl in Z2:
        for z in zl:
            if z < 50:
                l2.append(z)

    l3 = []
    for zl in Z3:
        for z in zl:
            if z < 50:
                l3.append(z)
    print(len(l1))
    print(len(l2))
    print(len(l3))
    '''
