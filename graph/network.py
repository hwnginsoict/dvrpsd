from .link import *
from .node import *

class Network():
    def __init__(self, customers: dict):
        self.depot = customers[0]
        self.num_nodes = len(customers)
        self.nodes = dict()     #link chua cac node, co ca node 0
        self.generate_node(customers)
        self.links = dict()    #links: dictionary luu cac link
        self.calculate_distance(customers)

        self.total_travel_time = 0  # objective 1
        self.accepted_dyn_req = 0 # objective 2

    def generate_node(self, customers):
        self.nodes = dict()
        for key, value in customers.items():  
            # print(type(value))  
            self.nodes[key] = value  

    def calculate_distance(self, customers): 
        for i in range(self.num_nodes):
            for j in range(i, self.num_nodes):
                self.links[(i,j)] = Link(customers[i], customers[j])
                self.links[(j,i)] = Link(customers[j], customers[i])
    
    def create_constraints(self):
        ...
