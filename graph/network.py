from .link import *
from .node import *

class Network():
    def __init__(self, input_path=None):
        self.input_path = input_path
        

        self.N = dict()
        self.L = dict()
        self.adj = dict()
        self.num_nodes = 0
        self.num_links = 0  
        self.total_travel_time = 0      
        ...
     
    def build_pheromone(self, num_sfcs = -1):
        self.pheromone = np.zeros((self.num_nodes, self.num_nodes))
        # for links
        for u, adj_u in self.adj.items():
            for v in adj_u.keys():
                self.pheromone[u][v] = 1
        # for nodes
        for node in self.N.values():
            if node.type:
                self.pheromone[node.id][node.id] = 1

        if num_sfcs != -1:
            self.pheromone = np.stack([self.pheromone]*num_sfcs, axis=0)
    
    def create_constraints(self):
        ...