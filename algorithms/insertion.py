import random
import copy

class Insertion:
    def __init__(self, route, max_capacity, network, mode='heuristics'):
        self.route = route
        
        self.max_capacity = max_capacity
        self.mode = mode
        self.network = network

    def insert_node(self, node):
        if self.mode == 'heuristics':
            for i in range(len(self.route)):
                copy_route = copy.deepcopy(self.route)
                n = random.randint(0, len(self.route))
                copy_route.insert(n, node)
                if(self.check_capacity() and self.check_time()):
                    return copy_route, True
                else:
                    return self.route, False
        
        if self.mode == 'sort':
            for i in range(1, len(self.route)):
                copy_route = copy.deepcopy(self.route)
                copy_route.insert(i, node)
                if(self.check_capacity() and self.check_time()):
                    return copy_route, True
            return self.route, False
                
    def insert_route(self, route2):
        if self.mode == 'heuristics':
            copy_route = copy.deepcopy(self.route)
            # while True:
            for i in range(len(route2)):
                n = random.randint(0, len(self.route))
                copy_route.insert(n, route2[i])

            return copy_route, True
                    
                # if(self.check_capacity() and self.check_time()):
                #     return copy_route, True
                # else:
                #     return self.route, False


    def check_capacity(self):
        #check capacity
        cap = 0
        for request in self.route:
            cap += request.demand
        if cap > self.max_capacity:
            return False
        return True
        
    def check_time(self):
        #check time window
        time = 0
        for i in range(len(self.route)-1):
            time = time + 0 + self.network.links[(self.route[i].node, self.route[i+1].node)].distance
            if time < self.route[i+1].start:
                time = self.route[i+1].start
            if time > self.route[i+1].end:
                return False
        return True