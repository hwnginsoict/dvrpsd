from ..graph import *

class Ant:
    def __init__(self, capacity, candidate_list, current_node = 0):
        self.current_node = current_node
        self.candidate_node = list() # đỉnh tiếp theo có thể ghé
        self.capacity = capacity # giảm dần trên tuyến đường
        self.route = list() # ghi lại tuyến đường đã đi
        self.visited = list()
        self.total_distance = 0 # chi phí thực hiện tuyến đường
    
    # def find_next(self, candidate_list): 
    #     while len(self.visited) < 
        
    def move(self, next_node, distance, demand):
        self.route.append(next_node)
        self.total_distance += distance
        self.capacity -= demand
        