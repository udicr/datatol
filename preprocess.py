import subprocess
import os
import shutil
import re
from distutils.dir_util import copy_tree
import sys
from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool(4)
#pbns = [i for i in range(1,54) if i not in [6,23,50,53]]
pbns = [1,2,3,4]
print(pbns)


def run(pb):
    '''
    run
    :return: output
    '''
    output = []
    strt = "Rscript preprocess.R "+str(pb)
    process = subprocess.Popen(strt, cwd=".",
                               stdout=subprocess.PIPE, shell=True)  # .stdout.decode('utf-8')
    for line in iter(process.stdout.readline, b''):
        l = line.decode('utf-8')
        sys.stdout.write(l)
        output.append(l.rstrip())

    return output

if __name__ == "__main__":
    results = pool.map(run,pbns)
    with open("preprocess_log1-4.txt","w") as file:
        for res in results:
            for r in res:
                file.write(r + "\n")


