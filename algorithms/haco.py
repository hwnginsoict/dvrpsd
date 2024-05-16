import numpy as np

from graph.network import Network
from graph.node import Node

from problem import Problem

from ls.search2 import Search2

import random

class HACO:
    def __init__(self, network, requests, max_capacity):
        self.network = network
        self.split_requests(requests)
        self.max_capacity = max_capacity
        self.set_parameter()

        self.generate_pheromone()
        
        self.static_routing()
        

    def set_parameter(self):
        self.num_ants = 100
        self.max_iteration = 50

        self.alpha = 1
        self.beta = 2
        self.rho = 0.1
        self.q = 150
        # self.

        self.best_distance = float('inf')
        self.best_solution = None

    def split_requests(self, requests): #tach request tinh, dong
        self.sta_requests = list()
        self.dyn_requests = list()
        for request in requests:
            if request.time == 0:
                self.sta_requests.append(request)
            else: self.dyn_requests.append(request)


    def static_routing(self):
        for i in range (self.max_iteration):
            solutions = list()
            candidate_list = list()
            for request in self.sta_requests:
                candidate_list.append(request)

            for request in self.dyn_requests: #test aco, remove later
                candidate_list.append(request)

            self.depot = candidate_list.pop(0)   #bo depot ra khoi candidate list

            print("hello this is", self.depot.node)



            for ant in range(self.num_ants):
                solution = [self.depot] #start from depot
                remain_capacity = self.max_capacity
                visited = set()

                solution_time = 0
                current_node = self.depot

                while len(visited) < len(self.sta_requests) + len(self.dyn_requests) -1:  # Visit all customers
                    probability = self.generate_probability(current_node, candidate_list, visited, remain_capacity, solution_time)

                    if len(probability) == 0:  # Check capacity constraint for vehicle
                        solution.append(self.depot)
                        current_node = self.depot
                        remain_capacity = self.max_capacity
                        solution_time = 0
                        continue

                    next_node = self.choose_next_node(probability)

                    # print("capa ", remain_capacity)
                    # print(next_node.node)

                    solution.append(next_node)
                    visited.add(next_node.node)
                    remain_capacity -= next_node.demand

                    solution_time += self.network.links[(current_node.node, next_node.node)].distance
                    solution_time = max(solution_time, next_node.start) #neu den som thi doi

                    if remain_capacity < 0:  # Check capacity constraint for vehicle
                        solution.pop()
                        solution.append(self.depot)
                        current_node = self.depot
                        remain_capacity = self.max_capacity
                        solution_time = 0
                        continue

                    current_node = next_node

                    # print(solution)


                solution.append(self.depot)  # Return to depot


                #test local search
                n = random.random()
                if n > 0.7:
                    n1 = random.randrange(0, len(solution))
                    n2 = random.randrange(0, len(solution))
                    temp1, temp2 = Search2.swap(solution[n1],solution[n2])
                    solution[n1] = temp1
                    solution[n2] = temp2
                    

                solutions.append(solution)
            
            self.update_pheromone(solutions)
        
            for solution in solutions:
                    distance = self.calculate_solution_distance(solution)
                    if distance < self.best_distance:
                        self.best_distance = distance
                        self.best_solution = solution

            # self.best_solution = best_solution
            # self.best_distance = best_distance

            print(i, end = " ")
            for i in range(len(self.best_solution)):
                print(self.best_solution[i].node, end = " ")
            print()
            print(self.best_distance)


    def generate_probability(self, current_node, candidate_list, visited, remain_capacity, solution_time):
        probability = list()
        total = 0
        for request in candidate_list: 
            if request.node not in visited:
                # if remain_capacity >= request.demand:
                if solution_time + self.network.links[(current_node.node, request.node)].distance < request.end:
                    if solution_time + self.network.links[(current_node.node, request.node)].distance >= request.start:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)*(self.network.links[(current_node.node,request.node)].distance)  #cong thuc toan hoc cua haco
                        probability.append((request,total))
                    else:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)*(self.network.links[(current_node.node,request.node)].distance 
                                                                                                 + request.end - (self.network.links[(current_node.node,request.node)].distance + solution_time))  #doi request bat dau
                        probability.append((request,total))

        probability = [(node, prob / total) for node, prob in probability]

        # if len(probability) == 0:
        #     return [(self.depot, 1)]

        return probability
    
    def choose_next_node(self, probability):
        r = np.random.rand()
        for node, prob in probability:
            if r <= prob:
                return node


    def generate_pheromone(self):
        # self.pheromone = dict()
        # for i in range(self.network.num_nodes):
        #     for j in range(self.network.num_nodes):
        #         self.pheromone[(i,j)] = 1
        self.pheromone = np.ones((self.network.num_nodes, self.network.num_nodes))

    def update_pheromone(self, solutions):
        delta_pheromone = np.zeros_like(self.pheromone)

        # print(self.pheromone)

        for solution in solutions:
            for i in range(len(solution) - 1):
                current_node = solution[i]
                next_node = solution[i + 1]
                delta_pheromone[current_node.node][next_node.node] += self.q / self.calculate_solution_distance(solution)

        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone

    def calculate_solution_distance(self, solution):
        distance = 0
        for i in range(len(solution)-1):
            distance += self.network.links[(solution[i].node,solution[i + 1].node)].distance
        return distance


if __name__ == "__main__":
    np.random.seed()
    problem1 = Problem("data/C100/C101.TXT")
    network = problem1.network
    requests = problem1.requests
    for request in requests:
        print(request.node)
    max_capacity = problem1.capacity
    haco = HACO(network = network, requests = requests, max_capacity = max_capacity)


