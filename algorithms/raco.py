from .ant import *
from ..graph import Link, Node, Network
from problem import Problem

import copy, time

class ACO:
    def __init__(self, problem: Problem, network: Network, time_slot = None):
        self.problem = problem
        self.network = copy.deepcopy(network)
        self.time_slot = time_slot
        self.ants = ... # set of ants, represent number of vehicle
        self.pheromone = ...
        self.reward_pheromone = ...
        self.evaporation_pheromone = ...
        
    def run(self):
        begin = time.time()
        
        # initialize ants + pheromone matrix
        self.ants, self.pheromone = self.initialization()
        self.solve_static()
        
        # find solution for static requests
        
        # deal with dynamic request 
        # Tại mỗi time_slot t sẽ có 1 request động đến và cần phải xử lý
        for t in range(1, self.time_slot):
            accepted_dyn_req = False # switch to True if dynaic request is accepted 
            
            # update pheromone 
            
            # update objectives
            self.calculate_objective(accepted_dyn_req)
            
        self.total_time = time.time() - begin
        
        return ...

    def initialization(self): # khởi tạo kiến và ma trận pheromone ban đầu
        # khởi tạo đàn kiến có kích cỡ bằng số vehicle, ban đầu tất cả kiến đều ở depot, chưa bị giảm capacity
        ants = dict()
        for i in range(self.problem.num_vehicle):
            ants[i] = Ant(current_node=self.network.nodes[0], capacity=self.problem.capacity)
            
        # khởi tạo ma trận pheromone ban đầu
        pheromone_matrix = ...
        return ants, pheromone_matrix 
        
    def solve_static(self):
        ...
        
    def solve_dynamic(self):
        ...        
    
    def calculate_objective(self, accepted_dyn_req):
        # first objective
        for ant in self.ants:
            self.network.total_travel_time +=  ant.travel_time()
        
        # second objective
        if accepted_dyn_req == True:
            self.network.accepted_dyn_req += 1
