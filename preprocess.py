import subprocess
import os
import shutil
import re
from distutils.dir_util import copy_tree
import sys

pb = 1


def run():
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


a = run()
