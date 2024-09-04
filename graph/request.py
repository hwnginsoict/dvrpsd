import numpy as np

class Request:
    def __init__(self, node: int, demand: float = None, start: float = None, end: float = None, servicetime: float = None, time: float = 0, drone_serve: bool = 1)-> None:
        self.node = node
        # self.demand = self.stochastic_demand(demand)
        self.demand = demand
        self.start = start
        self.end = end
        self.servicetime = servicetime
        self.time = time 
        self.drone_serve = drone_serve

        self.service_type = 'truck'

    
    def stochastic_demand(self, lda):
        num = np.random.poisson(lda)
        return num
    
    def to_drone(self):
        self.service_type = 'drone'
    
    def to_truckdrone(self):
        self.service_type = 'truckdrone'
    
if __name__ == "__main__":
    a = Request(1, 5, 10, 15, 0)
    print(a.time)
        
        
