from mimircache.profiler.generalProfiler import generalProfiler
from mimircache.profiler.heatmap import heatmap
from mimircache.profiler.cGeneralProfiler import cGeneralProfiler
from mimircache.const import *
from mimircache.profiler.twoDPlots import *
from mimircache.profiler.evictionStat import *
from mimircache.utils.prepPlotParams import *

class cachecow:
    def __init__(self, **kwargs):
        self.reader = None
        self.cacheclass_mapping = {}

    def open(self, file_path, data_type='c'):
        # assert os.path.exists(file_path), "data file does not exist"
        self.reader = plainReader(file_path, data_type=data_type)
        return self.reader

    def csv(self, file_path, init_params, data_type='c'):
        self.reader = csvReader(file_path, data_type=data_type, init_params=init_params)
        return self.reader

    def vscsi(self, file_path, data_type='v'):
        self.reader = vscsiReader(file_path, data_type=data_type)
        return self.reader

    def set_size(self, size):
        assert isinstance(size, int), "size can only be an integer"
        self.cache_size = size

    def num_of_request(self):
        return self.reader.get_num_of_total_requests()

    def reset(self):
        self.reader.reset()

    def _profiler_pre_check(self, **kwargs):
        """
        check whether user has provided new cache size and data information
        :param kwargs:
        :return:
        """
        reader = None

        if 'num_of_threads' in kwargs:
            num_of_threads = kwargs['num_of_threads']
        elif 'num_of_threads' in kwargs:
            num_of_threads = kwargs['num_of_threads']
        else:
            num_of_threads = DEFAULT_NUM_OF_THREADS

        if 'data' in kwargs and 'dataType' in kwargs:
            if kwargs['dataType'] == 'plain':
                reader = plainReader(kwargs['data'])
            if kwargs['dataType'] == 'csv':
                assert 'column' in kwargs, "you didn't provide column number for csv reader"
                reader = csvReader(kwargs['data'], kwargs['column'])
            if kwargs['dataType'] == 'vscsi':
                reader = vscsiReader(kwargs['data'])
        elif 'reader' in kwargs:
            reader = kwargs['reader']
        else:
            reader = self.reader

        assert reader!=None, "you didn't provide a reader nor data (data file and data type)"
        self.reader = reader

        return reader, num_of_threads

    def heatmap(self, mode, plot_type, time_interval=-1, num_of_pixels=-1,
                algorithm="LRU", cache_params=None, cache_size=-1, **kwargs):
        """

        :param mode:
        :param interval:
        :param kwargs: algorithm:
        :return:
        """

        reader, num_of_threads = self._profiler_pre_check(**kwargs)

        l = ["avg_rd_start_time_end_time", "hit_rate_start_time_cache_size"]

        if plot_type in l:
            hm = heatmap()
        else:
            if algorithm.lower() in c_available_cache:
                hm = cHeatmap()

            else:
                hm = heatmap()

        print(hm)
        print(kwargs)
        hm.heatmap(reader, mode, plot_type,
                   time_interval=time_interval,
                   num_of_pixels=num_of_pixels,
                   cache_size=cache_size,
                   algorithm=cache_alg_mapping[algorithm.lower()],
                   cache_params=cache_params,
                   **kwargs)

    def differential_heatmap(self, mode, plot_type, algorithm1, time_interval=-1, num_of_pixels=-1,
                             algorithm2="Optimal", cache_params1=None, cache_params2=None, cache_size=-1, **kwargs):
        """
        alg2 - alg1
        :param alg1:
        :param alg2:
        :param mode:
        :param interval:
        :param plot_type:
        :param kwargs:
        :return:
        """
        figname = 'differential_heatmap.png'
        if 'figname' in kwargs:
            figname = kwargs['figname']

        assert cache_size != -1, "you didn't provide size for cache"

        reader, num_of_threads = self._profiler_pre_check(**kwargs)

        if algorithm1.lower() in c_available_cache and algorithm2.lower() in c_available_cache:
            hm = cHeatmap()
            hm.differential_heatmap(reader, mode, plot_type,
                                    cache_size=cache_size,
                                    time_interval=time_interval,
                                    num_of_pixels=num_of_pixels,
                                    algorithm1=cache_alg_mapping[algorithm1.lower()],
                                    algorithm2=cache_alg_mapping[algorithm2.lower()],
                                    cache_params1=cache_params1,
                                    cache_params2=cache_params2,
                                    **kwargs)

        else:
            hm = heatmap()
            if algorithm1.lower() not in c_available_cache:
                xydict1 = hm.calculate_heatmap_dat(reader, mode, plot_type,
                                                   time_interval=time_interval,
                                                   cache_size=cache_size,
                                                   algorithm=algorithm1,
                                                   cache_params=cache_params1,
                                                   **kwargs)[0]
            else:
                xydict1 = c_heatmap.heatmap(reader.cReader, mode, plot_type,
                                            cache_size=cache_size,
                                            time_interval=time_interval,
                                            algorithm=algorithm1,
                                            cache_params=cache_params1,
                                            num_of_threads=num_of_threads)

            if algorithm2.lower() not in c_available_cache:
                xydict2 = hm.calculate_heatmap_dat(reader, mode, interval, plot_type,
                                                   # time_interval=interval,
                                                   cache_size=cache_size,
                                                   algorithm=algorithm2,
                                                   cache_params=cache_params2,
                                                   **kwargs)[0]
            else:
                xydict2 = c_heatmap.heatmap(reader.cReader, mode, plot_type,
                                            time_interval=time_interval,
                                            cache_size=cache_size,
                                            algorithm=algorithm2,
                                            cache_params=cache_params2,
                                            num_of_threads=num_of_threads)

            cHm = cHeatmap()
            text = "      differential heatmap\n      cache size: {},\n      cache type: ({}-{})/{},\n" \
                   "      time type: {},\n      time interval: {},\n      plot type: \n{}".format(
                cache_size, algorithm2, algorithm1, algorithm1, mode, time_interval, plot_type)

            x1, y1 = xydict1.shape
            x1 = int(x1 / 2.8)
            y1 /= 8
            if mode == 'r':
                cHm.set_plot_params('x', 'real_time', xydict=xydict1, label='start time (real)',
                                    text=(x1, y1, text))
                cHm.set_plot_params('y', 'real_time', xydict=xydict1, label='end time (real)', fixed_range=(-1, 1))
            else:
                cHm.set_plot_params('x', 'virtual_time', xydict=xydict1, label='start time (virtual)',
                                    text=(x1, y1, text))
                cHm.set_plot_params('y', 'virtual_time', xydict=xydict1, label='end time (virtual)', fixed_range=(-1, 1))

            # print(xydict2.shape)
            # print(xydict1.shape)
            np.seterr(divide='ignore', invalid='ignore')
            # print(xydict2 - xydict1)
            # print(xydict1)
            # print((xydict2 - xydict1) / xydict1)

            plot_dict = (xydict2 - xydict1) / xydict1

            # masked_array = np.ma.array((xydict2 - xydict1) / xydict1, mask=np.isnan((xydict2 - xydict1) / xydict1))
            # print(masked_array)
            # print(plot_dict)
            cHm.draw_heatmap(plot_dict, figname=figname)

    def profiler(self, algorithm, cache_params=None, cache_size=-1, **kwargs):
        """
        profiler
        :param cache_class:
        :param kwargs:
        :return:
        """

        reader, num_of_threads = self._profiler_pre_check(**kwargs)

        profiler = None
        bin_size = -1


        if algorithm.lower() == "lru":
            profiler = LRUProfiler(reader, cache_size)
        else:
            assert cache_size != -1, "you didn't provide size for cache"
            if 'bin_size' in kwargs:
                bin_size = kwargs['bin_size']

            if isinstance(algorithm, str):
                if algorithm.lower() in c_available_cache:
                    profiler = cGeneralProfiler(reader, cache_alg_mapping[algorithm.lower()], cache_size, bin_size,
                                                cache_params, num_of_threads)
                else:
                    profiler = generalProfiler(reader, self.cacheclass_mapping[algorithm.lower()], cache_size, bin_size,
                                               cache_params, num_of_threads)
            else:
                profiler = generalProfiler(reader, algorithm, cache_size, bin_size, cache_params, num_of_threads)

        return profiler

    def __iter__(self):
        assert self.reader, "you haven't provided a data file"
        return self.reader

    def next(self):
        return self.__next__()

    def __next__(self):  # Python 3
        return self.reader.next()

    def __del__(self):
        pass
        # if self.reader:
        #     self.reader.close()

    def twoDPlot(self, mode, time_interval, plot_type, **kwargs):
        if "figname" in kwargs:
            figname = kwargs['figname']
        else:
            figname = plot_type + ".png"
        if plot_type == 'cold_miss':
            cold_miss_2d(self.reader, mode, time_interval, figname=figname)
        elif plot_type == 'request_num':
            request_num_2d(self.reader, mode, time_interval, figname=figname)
        else:
            print("currently don't support your specified plot_type: " + str(plot_type))


    def evictionPlot(self, mode, time_interval, plot_type, algorithm, cache_size, cache_params=None, **kwargs):
        if plot_type == "reuse_dist":
            eviction_stat_reuse_dist_plot(self.reader, algorithm, cache_size, mode,
                                          time_interval, cache_params=cache_params, **kwargs)
        elif plot_type == "freq":
            eviction_stat_freq_plot(self.reader, algorithm, cache_size, mode, time_interval,
                                    accumulative=False, cache_params=cache_params, **kwargs)

        elif plot_type == "accumulative_freq":
            eviction_stat_freq_plot(self.reader, algorithm, cache_size, mode, time_interval,
                                    accumulative=True, cache_params=cache_params, **kwargs)
        else:
            print("the plot type you specified is not supported: {}, currently only support: {}".format(
                plot_type, "reuse_dist, freq, accumulative_freq"
            ))

    def plotHRCs(self, algorithm_list, cache_params=None, cache_size=-1, bin_size=-1, auto_size=True, **kwargs):
        plot_dict = prepPlotParams("Hit Rate Curve", "Cache Size/A.U.", "Hit Rate", "HRC.png", **kwargs)
        num_of_threads = 4
        if 'num_of_threads' in kwargs:
            num_of_threads=kwargs['num_of_threads']

        label = algorithm_list
        if 'label' in kwargs:
            label = kwargs['label']


        if auto_size:
            cache_size = LRUProfiler(self.reader).plotHRC(auto_resize=True, threshhold=0.98, no_save=True)
        if bin_size == -1:
            bin_size = cache_size // DEFAULT_BIN_NUM_PROFILER +1
        for i in range(len(algorithm_list)):
            alg = algorithm_list[i]
            if cache_params and i < len(cache_params):
                cache_param = cache_params[i]
            else:
                cache_param = None
            profiler = self.profiler(alg, cache_param, cache_size,
                                     bin_size=bin_size, num_of_threads=num_of_threads)
            hr = profiler.get_hit_rate()
            # if alg == "LRU":
            #     print(hr[cache_size])
            self.reader.reset()
            # plt.xlim(0, cache_size)
            if alg!="LRU":
                plt.plot([i*bin_size for i in range(len(hr))], hr, label=label[i])
            else:
                plt.plot(hr[:-2], label=label[i])

        plt.legend(loc="lower right")
        plt.xlabel(plot_dict['xlabel'])
        plt.ylabel(plot_dict['ylabel'])
        plt.title(plot_dict['title'], fontsize=18, color='black')
        if not 'no_save' in kwargs or not kwargs['no_save']:
            plt.savefig(plot_dict['figname'], dpi=600)
        colorfulPrint("red", "plot is saved at the same directory")
        try:
            plt.show()
        except:
            pass
        plt.clf()


    def plotMRCs(self, algorithm_list, cache_params=None, cache_size=-1, bin_size=-1, auto_size=True, **kwargs):
        plot_dict = prepPlotParams("Miss Rate Curve", "Cache Size/blocks.", "Miss Rate", "MRC.png", **kwargs)
        num_of_threads = 4
        if 'num_of_threads' in kwargs:
            num_of_threads = kwargs['num_of_threads']
        if 'label' not in kwargs:
            label = algorithm_list
        else:
            label = kwargs['label']
        ymin = 1

        if auto_size:
            cache_size = LRUProfiler(self.reader).plotMRC(auto_resize=True, threshhold=0.98, no_save=True)
        if bin_size == -1:
            bin_size = cache_size // DEFAULT_BIN_NUM_PROFILER +1
        for i in range(len(algorithm_list)):
            alg = algorithm_list[i]
            if cache_params and i < len(cache_params):
                cache_param = cache_params[i]
            else:
                cache_param = None
            profiler = self.profiler(alg, cache_param, cache_size,
                                     bin_size=bin_size, num_of_threads=num_of_threads)
            mr = profiler.get_miss_rate()
            ymin = min(ymin, max(min(mr)-0.02, 0))
            self.reader.reset()
            # plt.xlim(0, cache_size)
            if alg != "LRU":
                plt.plot([i * bin_size for i in range(len(mr))], mr, label=label[i])
            else:
                plt.plot(mr[:-2], label=label[i])

        print("ymin = {}".format(ymin))
        if "ymin" in kwargs:
            ymin = kwargs['ymin']

        plt.ylim(ymin=ymin)
        plt.semilogy()
        plt.legend(loc="upper right")
        plt.xlabel(plot_dict['xlabel'])
        plt.ylabel(plot_dict['ylabel'])
        plt.title(plot_dict['title'], fontsize=18, color='black')
        if not 'no_save' in kwargs or not kwargs['no_save']:
            plt.savefig(plot_dict['figname'], dpi=600)
        colorfulPrint("red", "plot is saved at the same directory")
        try:
            plt.show()
        except:
            pass
        plt.clf()


if __name__ == "__main__":
    CACHE_SIZE = 38000
    c = cachecow()
    # c.open('../data/trace.txt')
    # c.open("../data/test.dat")

    c.vscsi('../data/trace.vscsi')
    # c.vscsi('../data/traces/w38_vscsi1.vscsitrace')
    d = {"LRU_percentage": 0.3}
    # p = c.profiler("LRU_dataAware", cache_size=2000, cache_params=d, num_of_threads=8)
    # p = c.profiler("LRU")
    # print(p.__dict__)
    # p = c.profiler("LRU_K", cache_size=CACHE_SIZE, cache_params={"K": 2}, num_of_threads=8)
    # print(p.get_reuse_distance())
    # print((p.get_hit_rate()))
    # p.plotHRC(figname="w27_LRULFU_0.3_HRC.png", cache_size=2800000)
    c.differential_heatmap('v', 100, "hit_rate_start_time_end_time", algorithm1="LRU_2", algorithm2="Optimal",
                           # cache_params2={"LRU_percentage":0.3},
                           cache_size=2000, figname="differential_heatmap_LRU2_Opt_v.png",
                           num_of_threads=8)
    print(d)

    # p = c.profiler('optimal', cache_size=CACHE_SIZE)
    # print(p.get_hit_count())
    #
    # c.twoDPlot('v', 1000, "cold_miss")
    #
    # c.heatmap('r', 1000000, "hit_rate_start_time_end_time", "LRU", cache_size=CACHE_SIZE, num_of_threads=8,
    #           figname="abc.png")
    #
    # c.differential_heatmap('r', 1000000, "hit_rate_start_time_end_time", "LRU", cache_size=CACHE_SIZE, num_of_threads=8,
    #                        figname='2.png')
    #
    # c.differential_heatmap('r', 10000000, "hit_rate_start_time_end_time", "LRU", "ARC", cache_size=CACHE_SIZE,
    #                        num_of_threads=8, figname='3.png')
    #
    # # c.differential_heatmap('r', 1000000, "hit_rate_start_time_end_time", "LRU", num_of_threads=8, figname='2.png')
    #
    # TIME_INTERVAL = 10000000000
    # from mimircache.cacheReader.vscsiReader import vscsiCacheReader
    #
    # PATH = '/run/shm/traces/'
    # c = cachecow()
    #
    # for f in os.listdir(PATH):
    #     if f.endswith('vscsitrace'):
    #         # reader = vscsiCacheReader(PATH + f)
    #         c.vscsi(PATH + f)
    #         c.heatmap('r', TIME_INTERVAL, "rd_distribution",
    #                   figname='0627_rd_distribution/' + f + '_rd_distribution_' + str(TIME_INTERVAL) + '.png')
    #         # request_num_2d(reader, 'r', TIME_INTERVAL,
    #         #                figname='0627_rd_distribution/' + f + '_rd_distribution_' + str(TIME_INTERVAL) + '.png')
