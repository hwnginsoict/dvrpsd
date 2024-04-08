from .ant import *
from ..graph import Link, Node, Network

import copy, time

class ACO:
    def __init__(self, network: Network, time_slot = None):
        self.network = copy.deepcopy(network)
        self.time_slot = time_slot
        self.ants = ... # set of ants, represent number of vehicle
        self.pheromone = ...
        self.reward_pheromone = ...
        self.evaporation_pheromone = ...
        
    def run(self):
        begin = time.time()
        
        # initialize ants + pheromone matrix
        
        
        # find solution for static requests
        
        # deal with dynamic request 
        # Tại mỗi time_slot t sẽ có 1 request động đến và cần phải xử lý
        for t in range(1, self.time_slot):
            # update pheromone 
            ...
            
        self.total_time = time.time() - begin
        
        return ...

    def initialization(self): # khởi tạo kiến và ma trận pheromone ban đầu
        ...
        
    def solve_static(self):
        ...
        
    def solve_dynamic(self):
        ...        