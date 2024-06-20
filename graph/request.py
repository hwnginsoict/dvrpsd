import numpy as np

class Request:
    def __init__(self, node: int, demand: float = None, start: float = None, end: float = None, time: float = 0, drone_serve: bool = 1)-> None:
        self.node = node
        # self.demand = self.stochastic_demand(demand)
        self.demand = demand
        self.start = start
        self.end = end
        self.time = time
        self.drone_serve = drone_serve

    
    def stochastic_demand(self, lda):
        num = np.random.poisson(lda)
        return num
    
if __name__ == "__main__":
    a = Request(1, 5, 10, 15, 0)
    print(a.time)
        
        
