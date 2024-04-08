from ..graph import *

class Ant:
    def __init__(self):
        self.current_node = ...
        self.candidate_node = ... # đỉnh tiếp theo có thể ghé
        self.visited_node = ...
        self.capacity = ... # giảm dần trên tuyến đường
        self.route = [] # ghi lại tuyến đường đã đi
        self.cost = 0 # chi phí thực hiện tuyến đường
    
    def find_next_node(self): 
        ...
        
    def update_move(self):
        ...
        