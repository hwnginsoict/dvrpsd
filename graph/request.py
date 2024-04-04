import numpy as np

class Request:
    def __init__(self, node: int, demand: float = None, start: float, end: float, time: float=0)-> None:
        self.node = node
        self.demand = self.stochastic_demand(demand)
        self.start = start
        self.end = end
        self.time = time
    
    def stochastic_demand(self, lambda):
        num = np.random.poisson(lambda)
        return num
        
        
