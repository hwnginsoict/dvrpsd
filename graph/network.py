from .link import *
from .node import *

class Network():
    def __init__(self, customers: dict):
        self.depot = customers[0]
        self.num_nodes = len(customers)
        self.nodes = dict()     #link chua cac node, co ca node 0
        self.generate_node(customers)
        self.calculate_distance(customers)

        self.total_travel_time = 0  # objective 1
        self.accepted_dyn_req = 0 # objective 2
        self.WAER = 1.2603 # kg/mile
        self.PGFER = 0.0003773 # kg/Wh
        self.AER = 3.3333 # Wh/mile

        self.calculate_upper(customers)
        # self.truck = truck

    def generate_node(self, customers):
        self.nodes = dict()
        for key, value in customers.items():  
            # print(type(value))  
            self.nodes[key] = value  

    def calculate_distance(self, customers): 
        self.links = np.ones((self.num_nodes, self.num_nodes))
        for i in range(self.num_nodes):
            for j in range(i, self.num_nodes):
                if i==j: 
                    self.links[(i,j)] = float('inf')
                    self.links[(j,i)] = float('inf')
                else:
                    self.links[(i,j)] = Link(customers[i], customers[j]).distance
                    self.links[(j,i)] = Link(customers[j], customers[i]).distance

    # def calculate_time(self, customers):
    #     self.time = np.ones((self.num_nodes, self.num_nodes))
    #     for i in range(self.num_nodes):
    #         for j in range(i, self.num_nodes):
    #             self.time[i,j] = self.links[i,j]/

    def calculate_upper(self, request_list):
        sum_max_dis = 0
        for i in range (1, len(request_list)):
            max_each_request = 0
            for j in range(1, len(request_list)):
                if i != j:
                    max_each_request = max(max_each_request, self.links[request_list[i].id, request_list[j].id])
            sum_max_dis += max_each_request
        depo_max = 0
        for i in range(len(request_list)):
            depo_max = max(depo_max, self.links[0, request_list[i].id])

        num_vehicle = 10
        sum_max_dis  = sum_max_dis + 2*depo_max*num_vehicle

        self.carbon_upper = sum_max_dis*self.WAER
        self.reject_upper = len(request_list)

    
    def create_constraints(self):
        ...
