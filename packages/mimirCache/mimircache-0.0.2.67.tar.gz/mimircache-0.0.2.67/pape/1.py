# coding=utf-8

"""
dat

w94: total 10688305, unique 251245
 0: 0.17924, 0.00000(2512, 0)
AMP:
 1: 0.72498, 0.74925(2512, 7844769)
 2: 0.68331, 0.87896(2512, 6154613)
 3: 0.65848, 0.89586(2512, 5737447)
 4: 0.63976, 0.92269(2512, 5347709)
 5: 0.62352, 0.93756(2512, 5074238)
 6: 0.60438, 0.95801(2512, 4749087)
 7: 0.58329, 0.97501(2512, 4432401)
 8: 0.57643, 0.97810(2512, 4342788)
mimir:
 0: 0.60341, 0.32061(2366, 14575294)
 1: 0.90895, 0.76573(2367, 10303197)
 2: 0.82402, 0.89301(2374, 7775530)
 3: 0.81855, 0.90777(2377, 7579364)
 4: 0.63869, 0.92394(2404, 5350951)
 5: 0.66921, 0.93051(2387, 5661908)
 6: 0.55605, 0.93462(2435, 4337209)
 7: 0.55412, 0.93659(2436, 4304913)
 8: 0.51291, 0.94214(2437, 3806053)
 9: 0.51132, 0.94364(2438, 3781438)
10: 0.49106, 0.94460(2448, 3546714)
11: 0.48130, 0.94757(2445, 3423021)


msr_prxy.txt: total 202853759, unique 258457
 0: 0.65336, 0.00000(2584, 0)
AMP:
 1: 0.69057, 0.56675(2584, 22582935)
 2: 0.66115, 0.58487(2584, 7116558)
 3: 0.65961, 0.68920(2584, 3775923)
 4: 0.65899, 0.75673(2584, 2854453)
 5: 0.65434, 0.64803(2584, 1005290)
 6: 0.65563, 0.83889(2584, 623201)
 7: 0.65555, 0.88732(2584, 538296)
 8: 0.65549, 0.97531(2584, 448950)
mimir:
 0: 0.74089, 0.29896(2434, 95040419)
 1: 0.88252, 0.66973(2441, 81760594)
 2: 0.93151, 0.98348(2535, 58777894)
 3: 0.92207, 0.98701(2537, 56258510)
 4: 0.92376, 0.98755(2535, 56545348)
 5: 0.90988, 0.98346(2536, 53893088)
 6: 0.90810, 0.98456(2541, 53330353)
 7: 0.89434, 0.98208(2542, 50592005)
 8: 0.89813, 0.98358(2536, 51314187)
 9: 0.88363, 0.98193(2536, 48379737)
10: 0.87243, 0.98446(2540, 45813225)
11: 0.86702, 0.98467(2535, 44684742)
"""

dat_HR_PE_w94  = None
dat_HR_PE_prxy = None


import socket
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mimircache import *




dat_traces_sources = []
best_cache_sizes = [40000, 2000]
NUM_OF_THREADS = 8


if "Z240" in socket.gethostname():
    dat_traces_sources = ["/home/jason/ALL_DATA/cloudphysics_txt_64K/w94.txt",
                  "/home/jason/ALL_DATA/msr_txt_64K/msr_prxy.txt"]
elif "euler" in socket.gethostname():
    dat_traces_sources = ["w94.txt", "prxy.txt"]
    NUM_OF_THREADS = 32


def test_to_find_cache_size(dat):
    c = cachecow()
    c.open(dat)






def calHRC_Mithril(dat, cache_size):
    c = cachecow()
    c.open(dat)

    figname = dat[dat.rfind('/')+1 : dat.rfind('.')] + "_HRCs.png"
    c.plotHRCs(["LRU", "mimir", "PG", "Optimal"], # cache_size=12000, auto_size=False)
                cache_params=[None,
                              {
                                 "max_support": 12,
                                 "min_support":3,
                                 "confidence": 0,
                                 "item_set_size": 20,
                                 "prefetch_list_size": 2,
                                 "cache_type": "LRU",
                                 "sequential_type": 0,
                                 "max_metadata_size": 0.1,
                                 "block_size": 64 * 1024,
                                 "sequential_K": 0,
                                 "cycle_time": 2,
                                 "AMP_pthreshold":256
                              },
                              {
                                  "lookahead": 1,
                                  "cache_type": "LRU",
                                  "max_metadata_size": 0.1,
                                  "prefetch_threshold": 0.4,
                                  "block_size": 64 * 1024,
                              },
                              None],
               figname=figname, num_of_threads=NUM_OF_THREADS, cache_size=cache_size, auto_size=False)


def calHRC_LRU(dat):
    c = cachecow()
    c.open(dat)
    p = c.profiler("LRU")
    hr = p.get_hit_rate()[:-2]
    with open("dat1122/dat_HR_{}_LRU".format(dat[dat.rfind('/')+1:dat.rfind('.')]), 'w') as ofile:
        for s, i in enumerate(hr):
            ofile.write("{}: {}\n".format(s, i))


def cal_HRC_FIFO_OPT(dat, cache_size):
    bin_size = cache_size//200+1
    c = cachecow()
    c.open(dat)
    p_FIFO = c.profiler("FIFO", cache_size=cache_size, bin_size=bin_size, num_of_threads=NUM_OF_THREADS)
    p_OPT = c.profiler("FIFO", cache_size=cache_size, bin_size=bin_size, num_of_threads=NUM_OF_THREADS)
    hr_FIFO = p_FIFO.get_hit_rate()
    hr_OPT = p_OPT.get_hit_rate()

    with open("dat1122/dat_HR_{}_FIFO".format(dat[dat.rfind('/')+1:dat.rfind('.')]), 'w') as ofile:
        for s, i in enumerate(hr_FIFO):
            ofile.write("{}: {}\n".format(s*bin_size, i))

    with open("dat1122/dat_HR_{}_OPT".format(dat[dat.rfind('/') + 1:dat.rfind('.')]), 'w') as ofile:
        for s, i in enumerate(hr_OPT):
            ofile.write("{}: {}\n".format(s * bin_size, i))


def calHRC_PG(dat, cache_size):
    bin_size = cache_size//200+1
    c = cachecow()
    c.open(dat)
    p = c.profiler("PG", cache_size=cache_size, bin_size=bin_size,
                   cache_params={
                                "lookahead": 1,
                                "cache_type": "LRU",
                                "max_metadata_size": 0.1,
                                "prefetch_threshold": 0.5,
                                "block_size": 64 * 1024,
                    }, num_of_threads = NUM_OF_THREADS)
    hr = p.get_hit_rate()

    # with open("dat1122/dat_HR_{}_LRU".format(dat[dat.rfind('/')+1:dat.rfind('.')]), 'w') as ofile:
    #     for s, i in enumerate(hr):
    #         ofile.write("{}: {}\n".format(s, i))

    # print(hr.shape)



def plotHRC_PE():
    ###### w94 ###########
    pass




if __name__ == "__main__":
    for dat, cache_size in zip(dat_traces_sources, best_cache_sizes):
        # if 'w94' not in dat:
        #     calHRC_Mithril(dat, cache_size)
        # calHRC_LRU(dat)
        # cal_HRC_FIFO_OPT(dat, cache_size)
        calHRC_PG(dat, cache_size)
        print("*"*120)
    # plotHRC_PE()

