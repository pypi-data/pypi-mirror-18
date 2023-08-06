import configparser
import os

from mimircache.cache.ARC import ARC
from mimircache.cache.FIFO import FIFO
from mimircache.cache.LRU import LRU
from mimircache.cache.MRU import MRU
from mimircache.cache.Optimal import Optimal
from mimircache.cache.Random import Random
from mimircache.cache.S4LRU import S4LRU
from mimircache.cache.SLRU import SLRU
from mimircache.cache.clock import clock
from mimircache.cacheReader.csvReader import csvReader
from mimircache.cacheReader.plainReader import plainReader
from mimircache.cacheReader.vscsiReader import vscsiReader

# global c_available_cache
c_available_cache = []
c_available_cacheReader = [plainReader, vscsiReader, csvReader]
cache_alg_mapping = {}
BASE_DIR = os.path.dirname(__file__)

DEFAULT_BIN_NUM_PROFILER = 100
DEFAULT_NUM_OF_THREADS = 4


def init():
    _init_C_available_modules()
    _init_cache_alg_mapping()


def _init_C_available_modules():
    config = configparser.ConfigParser()
    # print(BASE_DIR + '/conf')
    config.read(BASE_DIR + '/conf')
    if 'C_available_cache' in config.sections():
        c_available_cache.extend(config['C_available_cache'])
    else:
        raise RuntimeWarning("cannot find any cache module in C")

        # if 'C_available_reader' in config.sections():
        #     c_available_cacheReader.extend(config['C_available_reader'])
        # else:
        #     raise RuntimeWarning("cannot find any cacheReader module in C")





def _init_cache_alg_mapping():
    """
    match all possible cache replacement algorithm names(lower case) to available cache replacement algorithms
    :return:
    """

    cache_alg_mapping['optimal'] = 'Optimal'
    cache_alg_mapping['opt'] = "Optimal"

    cache_alg_mapping['rr'] = "Random"
    cache_alg_mapping['random'] = "Random"

    cache_alg_mapping['lru'] = "LRU"
    cache_alg_mapping['lfu'] = "LFU"

    cache_alg_mapping['fifo'] = "FIFO"

    cache_alg_mapping['arc'] = "ARC"

    cache_alg_mapping['clock'] = "clock"

    cache_alg_mapping['mru'] = "MRU"

    cache_alg_mapping['slru'] = "SLRU"
    cache_alg_mapping['s4lru'] = "S4LRU"

    cache_alg_mapping['lfu_rr'] = "LFU_RR"
    cache_alg_mapping['lfu_mru'] = "LFU_MRU"

    cache_alg_mapping['lru_k'] = "LRU_K"
    cache_alg_mapping['lru_2'] = "LRU_2"

    cache_alg_mapping['lru_lfu'] = "LRU_LFU"

    cache_alg_mapping['lru_dataaware'] = "LRU_dataAware"
    cache_alg_mapping['yjc'] = "YJC"
    cache_alg_mapping['mimir'] = 'mimir'

    cache_alg_mapping['test1'] = "test1"
    cache_alg_mapping['amp'] = "AMP"

    cache_alg_mapping['ms1'] = "MS1"
    cache_alg_mapping['ms2'] = "MS2"

    cache_alg_mapping['pg'] = "PG"


def cache_name_to_class(name):
    cache_class = None
    if name.lower() in cache_alg_mapping:
        cache = cache_alg_mapping[name.lower()]
        if cache == 'Random':
            cache_class = Random
        elif cache == 'SLRU':
            cache_class = SLRU
        elif cache == 'S4LRU':
            cache_class = S4LRU
        elif cache == 'ARC':
            cache_class = ARC
        elif cache == 'LRU':
            cache_class = LRU
        elif cache == "Optimal":
            cache_class = Optimal
        elif cache == 'FIFO':
            cache_class = FIFO
        elif cache == "MRU":
            cache_class = MRU
        elif cache == 'clock':
            cache_class = clock
        elif cache == 'FIFO':
            cache_class = FIFO

    if cache_class:
        return cache_class
    else:
        raise RuntimeError("cannot recognize given cache replacement algorithm " + str(name))

