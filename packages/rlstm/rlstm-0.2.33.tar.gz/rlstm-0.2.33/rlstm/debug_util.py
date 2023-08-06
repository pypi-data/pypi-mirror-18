''' Debugging utils
        - Timing code w/o repetitive code
'''

from datetime import datetime
from collections import defaultdict
import pdb


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
