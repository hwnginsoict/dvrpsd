from .ant import *
from ..graph import Link, Node, Network

import copy, time

class ACO:
    def __init__(self, network: Network, time_slot = None):
        self.network = copy.deepcopy(network)
        self.time_slot = time_slot
        
    def run(self):
        begin = time.time()
        
        # Tại mỗi time_slot t sẽ có 1 request động đến và cần phải xử lý
        for t in range(1, self.time_slot):
            ...
        self.total_time = time.time() - begin