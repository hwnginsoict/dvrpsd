import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

from graph.network import Network
from graph.node import Node

from problemtd import ProblemTD

from algorithms.ls.search2 import Search2
from algorithms.ls.search1 import Search1

from algorithms.insertion import Insertion

import random
import copy

class ACO:
    def __init__(self, problem):
        self.problem = problem
        self.network = problem.network
        self.split_requests(problem.requests)
        self.max_capacity = problem.truck.capacity
        self.set_parameter()
        self.generate_pheromone()
        self.static_routing()
        

    def set_parameter(self):
        self.num_ants = 100
        self.max_iteration = 100
        self.alpha = 1
        self.beta = 2
        self.rho = 0.6
        self.q = 700

        self.best_distance = float('inf')
        self.best_solution = None

    def split_requests(self, requests): #tach request tinh, dong
        self.sta_requests = list()
        for request in requests:
            if request.time == 0:
                self.sta_requests.append(request)
            else: self.sta_requests.append(request)


    def static_routing(self):
        for i in range (self.max_iteration):
            solutions = list()
            candidate_list = list()
            for request in self.sta_requests:
                candidate_list.append(request)

            self.depot = candidate_list.pop(0)   #bo depot ra khoi candidate list

            print("hello this is", self.depot.node)

            for ant in range(self.num_ants):
                solution = [[self.depot]] #start from depot
                pointer = 0 #index of current
                remain_capacity = self.max_capacity
                visited = set()

                solution_time = 0
                current_node = self.depot

                while len(visited) < len(self.sta_requests) -1: # + len(self.dyn_requests):  # Visit all customers
                    probability = self.generate_probability(current_node, candidate_list, visited, remain_capacity, solution_time)
                    # print(probability)

                    if len(probability) == 0:  # Check time window
                        # print("hello")
                        solution[pointer].append(self.depot)
                        pointer += 1
                        solution.append([self.depot])
                        current_node = self.depot
                        remain_capacity = self.max_capacity
                        solution_time = 0
                        continue

                    next_node = self.choose_next_node(probability)

                    # print("capa ", remain_capacity)
                    # print(next_node.node)

                    solution[pointer].append(next_node)
                    visited.add(next_node.node)
                    remain_capacity -= next_node.demand

                    solution_time += self.network.links[current_node.node][next_node.node] 
                    solution_time = max(solution_time, next_node.start) #neu den som thi doi

                    if remain_capacity < 0:  # Check capacity constraint for vehicle
                        solution[pointer].pop()
                        solution[pointer].append(self.depot)
                        pointer += 1
                        solution.append([self.depot])
                        current_node = self.depot
                        remain_capacity = self.max_capacity
                        solution_time = 0
                        continue

                    current_node = next_node

                    # print(solution)
                    # print(len(visited), len(self.sta_requests))

                if solution[pointer] == [self.depot]:
                    solution.pop()
                    solution[pointer-1].append(self.depot)

                else: solution[pointer].append(self.depot)  # Return to depot

                # self.print_routeTD(solution)

                

                solutions.append(solution)
            
            
            self.update_pheromone(solutions)
        
            for solution in solutions:
                distance = self.calculate_solution_distance(solution)
                # print(distance)
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_solution = solution
            
            print("Best: ", self.best_distance)
            self.print_routeTD(self.best_solution)
    
 
    def generate_probability(self, current_node, candidate_list, visited, remain_capacity, solution_time):
        probability = list()
        total = 0
        for request in candidate_list: 
            if request.node not in visited:
                # if remain_capacity >= request.demand:
                if solution_time + self.network.links[current_node.node][request.node]  < request.end:
                    if solution_time + self.network.links[current_node.node][request.node]  >= request.start:
                        total += (self.pheromone[current_node.node][request.node]**self.alpha)/((self.network.links[current_node.node][request.node] )**self.beta)  #cong thuc toan hoc cua haco
                        probability.append((request,total))
                    else:
                        total += (self.pheromone[current_node.node][request.node]**self.alpha)/((self.network.links[current_node.node][request.node]  
                                                                                                 + request.end - (self.network.links[current_node.node][request.node]  + solution_time))**self.beta)  #doi request bat dau
                        probability.append((request,total))

        if total == 0: return []
        probability = [(node, prob / total) for node, prob in probability]
    
        return probability
    
    def choose_next_node(self, probability):
        r = np.random.rand()
        for node, prob in probability:
            if r <= prob:
                # print(node.node)
                return node


    def generate_pheromone(self):
        self.pheromone = np.ones((self.network.num_nodes, self.network.num_nodes))

    def update_pheromone(self, solutions):
        delta_pheromone = np.zeros_like(self.pheromone)
        for solution in solutions:
            distance = self.calculate_solution_distance(solution)
            if distance == float('inf'): continue

            for i in range(len(solution)):
                for j in range(len(solution[i])-1):
                    current_node = solution[i][j]
                    next_node = solution[i][j+1]
                    delta_pheromone[current_node.node][next_node.node] += self.q / distance

        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone

        # self.pheromone =  (self.pheromone + delta_pheromone)

    def calculate_solution_distance(self, solution):

        if (solution == None): return float('inf')
        if not self.check_capacity(solution, self.max_capacity): return float('inf') 
        if not self.check_time(solution): return float('inf') 
        distance = 0
        for i in range(len(solution)):
            for j in range(len(solution[i])-1):
                # print(solution[i][j].node, solution[i][j+1].node)
                distance += self.network.links[solution[i][j].node][solution[i][j+1].node] 
        return distance

    
    def calculate_carbon_emission(self, solution): #version 1, only 1 drone for the route
        if not self.check_capacity(solution, self.max_capacity): return float('inf') 
        if not self.check_time(solution): return float('inf')
        # carbon_emission = 0
        truck_length= 0
        drone_length = 0
        truck_route = []
        drone_route = []
        for route in solution:
            current_request = route[0]
            for i in range(1,len(route)-1):
                # request = solution[i]
                if route[i].service_type == 'truck':
                    # truck_route.append(solution[i])
                    truck_length +=  self.network.links[(current_request.node, route[i].node)] 
                    current_request = route[i]
                if route[i].service_type == 'drone':
                    # drone_route.append(solution[i-1])
                    # drone_route.append(solution[i])
                    # drone_route.append(solution[i+1])
                    drone_length += self.network.links[(route[i-1].node, route[i].node)] 
                    drone_length += self.network.links[(route[i].node, route[i+1].node)] 
                    # current_request = request

        #calculate the length
        # for i in range(1,truck_route):
        #     truck_route += self.network.links[truck_route[i-1].node, truck_route[i]] 

        # for i in range(1,)

        carbon_emission = self.network.WAER * truck_length + self.network.PGFER * self.network.AER * drone_length
        return carbon_emission
    
    # def calculate_solution_distance(self, solution):
    #     return self.calculate_carbon_emission(solution)
    
    def check_capacity(self, route: list, max_capacity):
        #check capacity
        for i in range(len(route)):
            cap = 0
            for request in route[i]:
                # print(request)
                cap += request.demand
            if cap > max_capacity:
                print("sai cap")
                return False
        return True
        
    def check_time(self, route: list):
        #check time window
        time = 0
        for i in range(len(route)):
            time = 0
            for j in range(len(route[i])-1):
                time = time + 0 + self.network.links[route[i][j].node][route[i][j+1].node] 
                if time < route[i][j+1].start:
                    time = route[i][j+1].start
                if time > route[i][j+1].end:
                    # print("sai win")
                    return False
            # print('dung win')
        return True
    
    def print_route(self, route):
        #lam 1 function rieng
        for i in range(len(route)):
            for j in range(len(route[i])):
                print(route[i][j].node, end = ' ')
            print()

    def print_routeTD(self, route):
        for i in range(len(route)):
            for j in range(len(route[i])):
                if route[i][j].service_type == 'truck':
                    print(route[i][j].node, end = ' ')
                else: 
                    print(str(str(route[i][j].node) + '*'), end = ' ')
                    # raise Exception
            print()
    def count_request(self, solution):
        count = 0
        for route in solution:
            count += len(route) -1
        return count
            
if __name__ == "__main__":
    np.random.seed(1)
    problem1 = ProblemTD("F:\\CodingEnvironment\\dvrpsd\\data\\dvrptw\\100\\h100r102.csv")
    haco = ACO(problem1)