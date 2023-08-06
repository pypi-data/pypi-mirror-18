"""
this module provides the heatmap ploting engine, it supports both virtual time (fixed number of trace requests) and
real time, under both modes, it support using multiprocessing to do the plotting
currently, it only support LRU
the mechanism it works is it gets reuse distance from LRU profiler (parda for now)
"""

import logging
import math
import os
import pickle
from collections import deque
from multiprocessing import Array, Process, Queue

import matplotlib
import matplotlib.ticker as ticker
import numpy as np

from mimircache.cache.LRU import LRU
from mimircache.cacheReader.csvReader import csvReader
from mimircache.cacheReader.vscsiReader import vscsiReader
from mimircache.oldModule.pardaProfiler import pardaProfiler
from mimircache.utils.printing import *

DEBUG = True

__all__ = ("run", "draw", "prepare_heatmap_dat")

# heatmap gradient, only works in _calc_rd_count_subprocess
# HEATMAP_GRADIENT = 10000
LOG_NUM = 0


def _calc_hit_count(reuse_dist_array, cache_size, begin_pos, end_pos, real_start):
    """

    :rtype: count of hit
    :param reuse_dist_array:
    :param cache_size:
    :param begin_pos:
    :param end_pos: end pos of trace in current partition (not included)
    :param real_start: the real start position of cache trace
    :return:
    """
    hit_count = 0
    miss_count = 0
    for i in range(begin_pos, end_pos):
        if reuse_dist_array[i] == -1:
            # never appear
            miss_count += 1
            continue
        if reuse_dist_array[i] - (i - real_start) < 0 and reuse_dist_array[i] < cache_size:
            # hit
            hit_count += 1
        else:
            # miss
            miss_count += 1
    return hit_count


def _calc_hit_rate_subprocess(order, cache_size, break_points_share_array, reuse_dist_share_array, q):
    """
    the child process for calculating hit rate, each child process will calculate for
    a column with fixed starting time
    :param order: the order of column the child is working on
    :return: a list of result in the form of (x, y, hit_rate) with x as fixed value
    """

    result_list = []
    total_hc = 0
    for i in range(order + 1, len(break_points_share_array)):
        hc = _calc_hit_count(reuse_dist_share_array, cache_size, break_points_share_array[i - 1],
                             break_points_share_array[i], break_points_share_array[order])
        total_hc += hc
        hr = total_hc / (break_points_share_array[i] - break_points_share_array[order])
        result_list.append((order, i, hr))
    q.put(result_list)
    # return result_list


def _calc_avg_rd_subprocess(order, cache_size, break_points_share_array, reuse_dist_share_array, q):
    """
    the child process for calculating average reuse distance in each block, each child process will calculate for
    a column with fixed starting time
    :param order: the order of column the child is working on
    :return: a list of result in the form of (x, y, hit_rate) with x as fixed value
    """

    result_list = []
    rd = 0
    never_see = 0
    count = 0
    for i in range(order + 1, len(break_points_share_array)):
        # rd = 0
        # never_see = 0
        for j in range(break_points_share_array[i - 1], break_points_share_array[i]):
            if reuse_dist_share_array[j] != -1:
                rd += reuse_dist_share_array[j]
                count += 1
            else:
                never_see += 1
        # print("{}:{}:{}+{}".format(break_points_share_array[i]-break_points_share_array[i-1], count+never_see, count, never_see))

        # result_list.append((order, i, never_see))
        result_list.append((order, i, rd / (break_points_share_array[i] - break_points_share_array[order])))
        # if break_points_share_array[i]-break_points_share_array[order]-never_see != 0:
        #     result_list.append((order, i, rd/(break_points_share_array[i]-break_points_share_array[order]-never_see)))

    # print(never_see+len(rd))
    q.put(result_list)


def _calc_rd_count_subprocess(order, max_rd, break_points_share_array, reuse_dist_share_array, q):
    """
    the child process for calculating average reuse distance in each block, each child process will calculate for
    a column with fixed starting time
    :param order: the order of column the child is working on
    :return: a list of result in the form of (x, y, hit_rate) with x as fixed value
    """

    result_list = []
    # rd_bucket = [0]* HEATMAP_GRADIENT
    rd_bucket = [0] * int(math.log(max_rd, LOG_NUM) + 1)
    # never_see = 0
    # count = 0
    # gap = max_rd//HEATMAP_GRADIENT+1


    for j in range(break_points_share_array[order], break_points_share_array[order + 1]):
        if reuse_dist_share_array[j] != -1:
            if reuse_dist_share_array[j] == 0:
                rd_bucket[0] += 1
            else:
                rd_bucket[int(math.log(reuse_dist_share_array[j], LOG_NUM))] += 1

                # if reuse_dist_share_array[j] // gap < len(rd_bucket):
                #     rd_bucket[reuse_dist_share_array[j] // gap] += 1
                # else:
                #     rd_bucket[-1] += 1
    for i in range(len(rd_bucket)):
        result_list.append((order, i, rd_bucket[i]))

        # if rd_bucket[i]:
        #     result_list.append((order, i, math.log2(rd_bucket[i])))
        # else:
        #     result_list.append((order, i, 0))
    q.put(result_list)







class heatmap:
    def __init__(self, cache_class=LRU):
        self.cache_class = cache_class
        if not os.path.exists('temp/'):
            os.mkdir('temp')
        self.gap = 0


    def prepare_heatmap_dat(self, mode, reader, calculate=True):
        """
        prepare the data for plotting heatmap
        :param mode:   mode can be either virtual time(v) or real time(r)
        :param reader: for reading the trace file
        :param calculate: flag for checking whether we need to recalculate reuse distance and distribution table
        :return:
        """

        # assert isinstance(reader, vscsiCacheReader), "Currently only supports vscsiReader"
        reader.reset()

        reuse_dist_python_list = []
        break_points = []

        # for general cache replacement algorithm, uncomment the following
        # p = pardaProfiler(30000, reader)


        if calculate:
            # build profiler for extracting reuse distance (For LRU)
            p = pardaProfiler(30000, reader)
            # reuse distance, c_reuse_dist_long_array is an array in dtype C long type
            c_reuse_dist_long_array = p.get_reuse_distance()

            for i in c_reuse_dist_long_array:
                reuse_dist_python_list.append(i)

            if not os.path.exists('temp/'):
                os.makedirs('temp/')
            with open('temp/reuse.dat', 'wb') as ofile:
                pickle.dump(reuse_dist_python_list, ofile)

        else:
            # the reuse distance has already been calculated, just load it
            with open('temp/reuse.dat', 'rb') as ifile:
                reuse_dist_python_list = pickle.load(ifile)

            breakpoints_filename = 'temp/break_points_' + mode + str(self.interval) + '.dat'
            # check whether the break points distribution table has been calculated
            if os.path.exists(breakpoints_filename):
                with open(breakpoints_filename, 'rb') as ifile:
                    break_points = pickle.load(ifile)


        # check break points are loaded or not, if not need to calculate it
        if not break_points:
            if mode == 'r':
                break_points = self._get_breakpoints_realtime(reader, self.interval)
            elif mode == 'v':
                break_points = self._get_breakpoints_virtualtime(self.interval, len(reuse_dist_python_list))
            with open('temp/break_points_' + mode + str(self.interval) + '.dat', 'wb') as ifile:
                pickle.dump(break_points, ifile)

        # create share memory for child process
        reuse_dist_share_array = Array('l', len(reuse_dist_python_list), lock=False)
        for i, j in enumerate(reuse_dist_python_list):
            reuse_dist_share_array[i] = j

        break_points_share_array = Array('i', len(break_points), lock=False)
        for i, j in enumerate(break_points):
            break_points_share_array[i] = j


        # Jason: efficiency can be further improved by porting into Cython and improve parallel logic
        # Jason: memory usage can be optimized by not copying whole reuse distance array in each sub process
        map_list = deque()
        for i in range(len(break_points) - 1):
            map_list.append(i)

        func_pointer = _calc_hit_rate_subprocess
        func_pointer = _calc_avg_rd_subprocess
        func_pointer = _calc_rd_count_subprocess

        # create the array for storing results
        # result is a dict: (x, y) -> heat, x, y is the left, lower point of heat square
        if func_pointer == _calc_rd_count_subprocess:
            max_rd = max(reuse_dist_python_list)
            # print("max rd = %d"%max_rd)
            # self.gap = max_rd // HEATMAP_GRADIENT + 1
            param1 = max_rd
            # result = np.empty((len(break_points), HEATMAP_GRADIENT), dtype=np.float32)
            self._set_log_num(max_rd, len(break_points))
            result = np.empty((len(break_points), int(math.log(max_rd, LOG_NUM)) + 1), dtype=np.float32)
            result[:] = np.nan

        else:
            # (x,y) means from time x to time y
            param1 = self.cache_size
            array_len = len(break_points)
            result = np.empty((array_len, array_len), dtype=np.float32)
            result[:] = np.nan


        # new 0510
        q = Queue()
        process_pool = []
        process_count = 0
        result_count = 0
        map_list_pos = 0
        while result_count < len(map_list):
            if process_count < self.num_of_process and map_list_pos < len(map_list):

                # p = Process(target=_calc_hit_rate_subprocess, args=(map_list[map_list_pos], self.cache_size,
                #                                                     break_points_share_array, reuse_dist_share_array,
                #                                                     q))
                p = Process(target=func_pointer, args=(map_list[map_list_pos], param1,
                                                       break_points_share_array, reuse_dist_share_array,
                                                       q))

                # p = Process(target=_calc_hit_rate_subprocess_general, args=(map_list[map_list_pos], self.cache_size,
                #                                                   break_points_share_array, reader, q))


                p.start()
                process_pool.append(p)
                process_count += 1
                map_list_pos += 1
            else:
                rl = q.get()
                for r in rl:
                    result[r[0]][r[1]] = r[2]
                process_count -= 1
                result_count += 1
            print("%2.2f%%" % (result_count / len(map_list) * 100), end='\r')
        for p in process_pool:
            p.join()
        del reuse_dist_share_array
        del break_points_share_array

        # old 0510
        # with Pool(processes=self.num_of_process) as p:
        #     for ret_list in p.imap_unordered(_calc_hit_rate_subprocess, map_list,
        #                                      chunksize=10):
        #         count += 1
        #         print("%2.2f%%" % (count / len(map_list) * 100), end='\r')
        #         for r in ret_list:  # l is a list of (x, y, hr)
        #             result[r[0]][r[1]] = r[2]

        # print(result)
        with open('temp/draw', 'wb') as ofile:
            pickle.dump(result, ofile)

        return result

    def _set_log_num(self, max_rd, length):
        """
        find out the LOG_NUM that makes the number of pixels in y axis to match the number of pixels in x axis
        :param max_rd: maxinum reuse distance
        :param length: length of break points (also number of pixels along x axis)
        :return:
        """
        global LOG_NUM
        init_log_num = 10
        l2_prev = length
        while True:
            l2 = math.log(max_rd, init_log_num)
            if l2 > length > l2_prev:
                LOG_NUM = init_log_num
                # print(LOG_NUM)
                break
            l2_prev = l2
            init_log_num = (init_log_num - 1) / 2 + 1



    @staticmethod
    def _get_breakpoints_virtualtime(bin_size, total_length):
        """

        :param bin_size: the size of the group (virtual time slice)
        :param total_length: the total length of trace requests
        :return: a list of break points
        """
        break_points = []
        for i in range(total_length // bin_size):
            break_points.append(i * bin_size)
        if break_points[-1] != total_length - 1:
            break_points.append(total_length - 1)

        if (len(break_points)) > 10000:
            colorfulPrintWithBackground('yellow', 'blue', "number of pixels in one dimension are more than 10000, \
            exact size: %d, it may take a very long time, if you didn't intend to do it, \
            please try with a larger time stamp" % len(break_points))

        return break_points

    @staticmethod
    def _get_breakpoints_realtime(reader, interval):
        """
        given reader(vscsi) and time interval, split the data according to the time interval,
        save the order into break_points(list)
        :param reader:
        :param interval:
        :return:
        """
        reader.reset()
        break_points = []
        prev = 0
        for num, line in enumerate(reader.lines()):
            if (float(line[0]) - prev) > interval:
                break_points.append(num)
                prev = float(line[0])

        # noinspection PyUnboundLocalVariable
        if line[0] != prev:
            # noinspection PyUnboundLocalVariable
            break_points.append(num)

        if (len(break_points)) > 10000:
            colorfulPrintWithBackground('yellow', 'blue', "number of pixels in one dimension are more than 10000, \
            exact size: %d, it may take a very long time, if you didn't intend to do it, \
            please try with a larger time stamp" % len(break_points))

        return break_points

    @staticmethod
    def _calc_hit_rate(reuse_dist_array, cache_size, begin_pos, end_pos):
        """
        the original function for calculating hit rate, given the reuse_dist_array, cache_size,
        begin position and end position in the reuse_dist_array, return hit rate
        now isolate as a separate function
        :param reuse_dist_array:
        :param cache_size:
        :param begin_pos:
        :param end_pos:
        :return:
        """
        hit_count = 0
        miss_count = 0
        for i in range(begin_pos, end_pos):
            if reuse_dist_array[i] == -1:
                # never appear
                miss_count += 1
                continue
            if reuse_dist_array[i] - (i - begin_pos) < 0 and reuse_dist_array[i] < cache_size:
                # hit
                hit_count += 1
            else:
                # miss
                miss_count += 1
        # print("hit+miss={}, total size:{}, hit rage:{}".format(hit_count+miss_count, \
        # end_pos-begin_pos, hit_count/(end_pos-begin_pos)))
        return hit_count / (end_pos - begin_pos)


    @staticmethod
    def draw(xydict, **kargs):
        if 'figname' in kargs:
            filename = kargs['figname']
        else:
            filename = 'heatmap.png'

        plt.clf()
        masked_array = np.ma.array(xydict, mask=np.isnan(xydict))

        # print(masked_array)
        cmap = plt.cm.jet
        cmap.set_bad('w', 1.)

        # fig = plt.figure()
        # ax = fig.add_subplot(111)

        # heatmap = plt.pcolor(result2.T, cmap=plt.cm.Blues, vmin=np.min(result2[np.nonzero(result2)]), \
        # vmax=result2.max())
        try:
            # ax.pcolor(masked_array.T, cmap=cmap)
            if 'fixed_range' in kargs and kargs['fixed_range']:
                img = plt.imshow(masked_array.T, vmin=0, vmax=1, interpolation='nearest', origin='lower')
            else:
                img = plt.imshow(masked_array.T, interpolation='nearest', origin='lower',
                                 norm=matplotlib.colors.LogNorm())
            cb = plt.colorbar(img)
            if 'text' in kargs:
                (length1, length2) = masked_array.shape
                ax = plt.gca()
                ax.text(length2 // 3, length1 // 8, kargs['text'], fontsize=20)  # , color='blue')

            # change tick from arbitrary number to real time
            if 'change_label' in kargs and kargs['change_label'] and 'interval' in kargs:
                ticks = ticker.FuncFormatter(lambda x, pos: '{:2.2f}'.format(x * kargs['interval'] / (10 ** 6) / 3600))
                plt.gca().xaxis.set_major_formatter(ticks)
                plt.gca().yaxis.set_major_formatter(ticks)
                plt.xlabel("time/hour")
                plt.ylabel("time/hour")

            if 'change_label_rd_bucket' in kargs and kargs['change_label_rd_bucket']:
                # ticks = ticker.FuncFormatter(lambda x, pos: '{:2.2f}'.format(x * kargs['interval'] / (10 ** 6) / 3600))
                ticks = ticker.FuncFormatter(lambda x, pos: '{:2.0f}'.format(LOG_NUM ** x))
                # plt.gca().xaxis.set_major_formatter(ticks)
                plt.gca().yaxis.set_major_formatter(ticks)
                plt.xlabel("logical time")
                plt.ylabel("reuse distance")


            # plt.show()
            plt.savefig(filename)
            colorfulPrint("red", "plot is saved at the same directory")
        except Exception as e:
            logging.warning(str(e))
            plt.pcolormesh(masked_array.T, cmap=cmap)
            plt.savefig(filename)

    def __del_manual__(self):
        """
        cleaning
        :return:
        """
        if os.path.exists('temp/'):
            for filename in os.listdir('temp/'):
                os.remove('temp/' + filename)
            os.rmdir('temp/')

    def run(self, mode, interval, cache_size, reader, **kargs):
        """

        :param mode:
        :param interval:
        :param cache_size:
        :param reader:
        :param kargs: include num_of_process, figname
        :return:
        """
        self.cache_size = cache_size
        self.interval = interval
        self.mode = mode
        if 'num_of_process' in kargs:
            self.num_of_process = kargs['num_of_process']
        else:
            self.num_of_process = 4


        if 'calculate' in kargs:
            calculate = kargs['calculate']
        else:
            calculate = True

        if mode == 'r':
            xydict = self.prepare_heatmap_dat('r', reader, calculate)
            kargs['interval'] = interval
        elif mode == 'v':
            xydict = self.prepare_heatmap_dat('v', reader, calculate)
        else:
            raise RuntimeError("Cannot recognize this mode, it can only be either real time(r) or virtual time(v), "
                               "but you input %s" % mode)

        if "change_label_rd_bucket" in kargs and kargs['change_label_rd_bucket']:
            kargs['gap'] = self.gap


        self.draw(xydict, **kargs)

        # self.__del_manual__()


def server_plot_all():
    import gc
    mem_sizes = []
    with open('memSize', 'r') as ifile:
        for line in ifile:
            mem_sizes.append(int(line.strip()))

    for filename in os.listdir("../data/cloudphysics"):
        print(filename)
        if filename.endswith('.vscsitrace'):
            if int(filename.split('_')[0][1:]) in [1, 3, 4, 5, 51, 99, 83, 87]:
                continue
            if os.path.exists(filename + '_rd_no_miss_r.png'):
                continue
            hm = heatmap()
            mem_size = mem_sizes[int(filename.split('_')[0][1:]) - 1] * 16
            reader = vscsiReader("../data/cloudphysics/" + filename)
            hm.run('r', 1000000000, mem_size, reader, num_of_process=48, figname=filename + '_rd_no_miss_r.png',
                   change_label='True')  # , fixed_range="True",
            del hm
            del reader
            gc.collect()


def server_size_plot():
    mem_sizes = []
    with open('memSize', 'r') as ifile:
        for line in ifile:
            mem_sizes.append(int(line.strip()))

    for filename in os.listdir("../data/cloudphysics"):
        if filename.endswith('.vscsitrace'):
            if int(filename.split('_')[0][1:]) in [1, 4, 5, 51, 99, 83, 87]:
                continue
            if os.path.exists('time_size/' + filename + '_512.png'):
                continue
            hm = heatmap()
            mem_size = mem_sizes[int(filename.split('_')[0][1:]) - 1]
            reader = vscsiReader("../data/cloudphysics/" + filename)
            print(filename)
            size = 512
            while size < mem_size * 1024 * 128:
                print(size)
                if size == 512:
                    hm.run('r', 1000000000, size, reader, num_of_process=42, figname='time_size/' + filename
                                                                                     + '_' + str(size) + '.png',
                           calculate=True, fixed_range=True, text='size=' + str(size))
                else:
                    hm.run('r', 1000000000, size, reader, num_of_process=42, figname='time_size/' + filename
                                                                                     + '_' + str(size) + '.png',
                           calculate=False, fixed_range=True, text='size=' + str(size))
                size *= 2


def server_request_num_plot():
    for filename in os.listdir("../data/cloudphysics"):
        print(filename)
        if filename.endswith('.vscsitrace'):
            if int(filename.split('_')[0][1:]) in [1, 4, 5, 51, 99, 83, 87]:
                continue
            if os.path.exists(filename + '_request_num.png'):
                continue
            hm = heatmap()
            reader = vscsiReader("../data/cloudphysics/" + filename)
            break_points = hm._get_breakpoints_realtime(reader, 1000000000)

            array_len = len(break_points)
            result = np.empty((array_len, array_len), dtype=np.float32)
            result[:] = np.nan

            for o1, i in enumerate(break_points):
                for o2, j in enumerate(break_points):
                    if i >= j:
                        continue
                    else:
                        result[o1][o2] = j - i
            hm.draw(result, figname=filename + '_request_num.png')


def server_plot_all_redis():
    for filename in os.listdir("../data/redis/"):
        print(filename)
        if filename.endswith('.csv'):
            reader = csvReader("../data/redis/" + filename, column=1)
            # print(reader)
            # for line in reader:
            #     print(line)
            #     break

            if filename in []:
                continue
            if os.path.exists(filename + '_r.png'):
                continue
            hm = heatmap()
            reader = csvReader("../data/redis/" + filename, column=1)
            hm.run('r', 20, 2000, reader, num_of_process=48, figname=filename + '_r.png',
                   fixed_range="True")  # , change_label='True')





def localtest():
    # reader1 = plainCacheReader("../data/parda.trace")



    reader2 = vscsiReader("../data/trace_CloudPhysics_bin")

    hm = heatmap()
    hm.run('r', 10000000, 2000, reader2, num_of_process=8, change_label_rd_bucket=True)  # ,change_label='False'
    # fixed_range=True, text="Hello word",
    del hm
    # p = pardaProfiler(20000, reader2)
    # p.run()



if __name__ == "__main__":
    import time

    t1 = time.time()
    localtest()
    t2 = time.time()
    print(t2 - t1)

    # server_plot_all()
    # server_plot_all_redis()
    # server_size_plot()
    # server_request_num_plot()
