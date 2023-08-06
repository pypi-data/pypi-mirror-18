''' Debugging utils
        - Timing code w/o repetitive code
'''

from datetime import datetime
from collections import defaultdict
import os
import pdb
import psutil


def getCurMemCost_MiB():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem_MiB = process.memory_info_ex().rss / float(2 ** 20)
    return mem_MiB


class MemTracker(object):
    def __init__(self):
        self.database = defaultdict(lambda: {
            'cost': 0,
            'avg_cost': 0,
            '_total_cost': 0,
            'n_steps': 0
        })

    def add(self, key):
        self.database[key]['cost'] = getCurMemCost_MiB()
        self.database[key]['n_steps'] += 1
        self.database[key]['_total_cost'] += self.database[key]['cost']
        self.database[key]['avg_cost'] += float(self.database[key]['_total_cost']) / self.database[key]['n_steps']


class Timer(object):
    def __init__(self):
        self.database = defaultdict(lambda: {'mode': 0, 'length': 0, 'total': 0})

    def start(self, key):
        self.database[key]['mode'] = 1
        self.database[key]['start'] = datetime.now()

    def end(self, key):
        assert self.database[key]['mode'] == 1, \
            'start timer for <{}> before ending'.format(key)

        self.database[key]['mode'] = 0
        self.database[key]['end'] = datetime.now()
        sub = self.database[key]['end'] - self.database[key]['start']
        self.database[key]['length'] = sub.microseconds
        self.database[key]['total'] += sub.microseconds

    def get(self, key):
        return self.database[key]['length']

