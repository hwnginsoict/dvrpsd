import random
import copy
class Search2:
    def __init__(self, route1: list, route2: list):
        self.route1 = route1
        self.route2 = route2
    
    def swap(self):
        copy_route1 = copy.deepcopy(self.route1)
        copy_route2 = copy.deepcopy(self.route2)
        n1 = int(random.random()*(len(self.route1)-1))
        n2 = int(random.random()*(len(self.route2)-1))
        temp = copy_route1[n1]
        copy_route1[n1] = copy_route2[n2]
        copy_route2[n2] = temp
        return copy_route1, copy_route2
