# coding=utf-8

import os, sys
from mimircache import *



NUM_OF_THREADS = 30

def plotHRCs(folder):
    c = cachecow()
    for f in os.listdir(folder):
        c.open("{}/{}".format(folder, f))
        c.plotHRCs(["LRU", "FIFO", "Optimal"], figname="{}/{}.png".format(folder, f), num_of_threads=NUM_OF_THREADS)



if __name__ == "__main__":
    plotHRCs("/var/dept/scratch/jyan254/cache/mimircache/utils/w65")