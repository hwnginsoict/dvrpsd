import copy
import random

class Search1:
    def __init__(self, route: list, max_capacity, candidate_list):
        self.route = route
        self.max_capacity = max_capacity
        self.candidate_list = candidate_list

    def search1(self, route: list):
        copy_route = copy.deepcopy(route)

        if check_capacity(copy_route, self.max_capacity) and check_time(copy_route, self.candidate_list):
            return copy_route
        else: return route


    def check_capacity(self, route: list, max_capacity):
        #check capacity
        cap = 0
        for request in route:
            cap += request.demand
        if cap > max_capacity:
            return False
        return True
        
    def check_time(self, route: list, candidate_list):
        #check time window
        copy_route = copy.deepcopy(route)
        time = 0
        for i in range(len(copy_route)-1):
            time = time + s_time[copy_route[i]] + distance(copy_route[i], copy_route[i+1])
            if time < e_time[copy_route[i+1]]:
                time = e_time[route2[i+1]]
            if time > l_time[route2[i+1]]:
                return False
        return True

