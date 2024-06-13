import copy
import random

class Search1:
    def __init__(self, route: list, max_capacity, network):
        self.route = route
        self.max_capacity = max_capacity
        self.network = network

    def search1(self):
        copy_route = copy.deepcopy(self.route)
        n1 = int(random.random()*(len(self.route)-1))
        n2 = int(random.random()*(len(self.route)-1))
        temp = copy_route[n1]
        copy_route[n1] = copy_route[n2]
        copy_route[n2] = temp
        if self.check_capacity(copy_route, self.max_capacity) and self.check_time(copy_route):
            return copy_route
        else: return self.route

    def calculate_solution_distance(self, solution):
        if self.check_capacity(solution, self.max_capacity) and self.check_time(solution): return float('inf')
        distance = 0
        for i in range(len(solution)-1):
            distance += self.network.links[(solution[i].node,solution[i + 1].node)].distance
        return distance

    def check_capacity(self, route: list, max_capacity):
        #check capacity
        cap = 0
        for request in route:
            cap += request.demand
        if cap > max_capacity:
            return False
        return True
        
    def check_time(self, route: list):
        #check time window
        time = 0
        for i in range(len(route)-1):
            time = time + route[i].start + self.network.links[(route[i].node, route[i+1].node)].distance
            if time < route[i+1].start:
                time = route[i+1].start
            if time > route[i+1].end:
                return False
        return True

