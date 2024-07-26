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

class TD_DACO:
    def __init__(self, problem):
        self.network = problem.network
        self.split_requests(problem.requests)
        self.max_capacity = problem.truck.capacity

        self.set_parameter()
        self.generate_pheromone()
        
        self.static_routing()
        self.dynamic_routing(40)
        
        

    def set_parameter(self):
        self.num_ants = 200
        self.max_iteration = 50

        self.alpha = 1
        self.beta = 2
        self.rho = 0.6
        self.q = 100

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

            """
            for request in self.dyn_requests: #test aco, remove later
                candidate_list.append(request)
            """

            self.depot = candidate_list.pop(0)   #bo depot ra khoi candidate list

            # print("hello this is", self.depot.node)

            for ant in range(self.num_ants):
                solution = [[self.depot]] #start from depot
                pointer = 0 #index of current
                remain_capacity = self.max_capacity
                visited = set()

                solution_time = 0
                current_node = self.depot

                while len(visited) < len(self.sta_requests) -1: # + len(self.dyn_requests):  # Visit all customers
                    probability = self.generate_probability(current_node, candidate_list, visited, remain_capacity, solution_time)

                    if len(probability) == 0:  # Check capacity constraint for vehicle
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

                    solution_time += self.network.links[(current_node.node, next_node.node)].distance
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


                solution[pointer].append(self.depot)  # Return to depot


                # test insertion

                # if True:
                #     n1 = int(random.random()*(len(solution)-1))
                #     n2 = int(random.random()*(len(solution)-1))
                #     while n2 == n1:
                #         n2 = int(random.random()*(len(solution)-1))
                #     if len(solution[n1]) < len(solution[n2]):
                #         n1, n2 = n2, n1

                #     n = int(random.random()*(len(solution[n2])-1))
                #     temp, cd = Insertion(route = solution[n1], max_capacity = self.max_capacity, network = self.network).insert_node(node = solution[n2][n])
                #     if cd == True:
                #         del solution[n2][n]
                #         solution[n1] = temp

                """
                if True:
                    n1 = int(random.random()*(len(solution)-1))
                    n2 = int(random.random()*(len(solution)-1))
                    while n2 == n1:
                        n2 = int(random.random()*(len(solution)-1))
                    if len(solution[n1]) < len(solution[n2]):
                        n1, n2 = n2, n1

                    temp, cd = Insertion(route = solution[n1], max_capacity = self.max_capacity, network = self.network).insert_route(solution[n2])
                    if cd == True:
                        del solution[n2]
                        solution[n1] = temp
                """

                #sua sau
                """
                n = random.random()
                if n > 0.8:
                    solution = Search1(solution,self.max_capacity,self.network).search1()

                for i in range(len(solution)):
                    print(solution[i].node, end= " ")
                print()
                """

                solutions.append(solution)
                

                #test local search
                # n = random.random()
                # if n > 0.8 and len(solutions) > 3:
                #     n1 = int(random.random()*(len(solutions)-1))
                #     n2 = int(random.random()*(len(solutions)-1))
                #     # print(n1, n2)
                #     while n2 == n1:
                #         n2 = int(random.random()*(len(solutions)-1))
                #         # print(n2)
                #     search2 = Search2(solutions[n1],solutions[n2])
                #     temp1, temp2 = search2.swap()
                #     solutions[n1] = temp1
                #     solutions[n2] = temp2


            # print(solutions)
            
            self.update_pheromone(solutions)
        
            for solution in solutions:
                distance = self.calculate_solution_distance(solution)
                # print(distance)
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_solution = solution

            # self.best_solution = best_solution
            # self.best_distance = best_distance

            
            # print("Best: ", self.best_distance)
            # self.print_route(self.best_solution)
            

        # print(self.pheromone)
    
    def dynamic_routing(self, timestep):
        timestep = 20
        time = self.depot.start
        # coming_request = self.dyn_requests #coming requests are requests havent received yet
        coming_request = []
        for request in self.dyn_requests:
            coming_request.append(request)
        handling_request = [] #handling requests are requests that are not assigned 
        for request in self.sta_requests:
            if request.node == 0: continue
            handling_request.append(request)
        all_request = []
        self.routes = sorted(self.best_solution, key = len)
        #self.planning_route = copy.deepcopy(self.routes) #to calculate total cost
        self.planning_route = []
        for route in self.routes:
            self.planning_route.append(route)
        self.present_route = [] #assigned requests
        self.coming_route = [] #planning unassigned requests

        for i in range(len(self.planning_route)):
            # self.present_route.append([self.depot,self.planning_route[i][1]])
            self.present_route.insert(0,[self.depot,self.planning_route[i][1]])
            for request in handling_request:
                if request.node == self.planning_route[i][1].node:
                    handling_request.remove(request)

        assigned = [0]
        while (time < self.depot.end):

            for route in self.present_route:
                for request in route:
                    if request.node not in assigned:
                        assigned.append(request.node)

            for i in self.dyn_requests:
                if i.node == 0: continue 
                if i.time < time and (i not in handling_request) and (i.node not in assigned):
                    handling_request.append(i)
                    all_request.append(i)
                    # print(i.node)
                    # for request in self.dyn_requests:
                    #     print(request.node, end = " ")
                    # print()

                    # for request in coming_request:
                    #     print(request.node, end = " ")
                    # print()

                    print("HANDLING")
                    for request in handling_request:
                        print(request.node, end =" ")
                    print()
                    print("HANDLING")

                    # print(i.node)

                    if i in coming_request:
                        coming_request.remove(i)
                # else: break          
            
            # for i in handling_request:
            #     print(i.node, end = ' ')
            # print()

            # if len(handling_request) ==0 : print('bewhdbfwhebfrwbgurbgiurwebguirwvb')

            
            # xu li dinh tuyen lai bang ACO, xu li tren coming_route
            for ants in range(self.num_ants):
                solution = copy.deepcopy(self.present_route)
                pointer = 0
                remain_capacity = sum(i.demand for i in solution[pointer])
                visited = set()
                current_node = self.present_route[pointer][-1]
                if self.present_route[pointer][-1].node == 0:
                    solution_time = time
                else: 
                    route_time = 0
                    for j in range(1, len(self.present_route[pointer])):
                        route_time += self.network.links[(self.planning_route[pointer][j-1].node,self.planning_route[pointer][j].node)].distance
                        route_time = max(route_time, self.planning_route[pointer][j].start)
                    solution_time = route_time

                candidate_list = copy.deepcopy(handling_request)
                solutions = []

            

                ite=1
                feasible = True
                while len(visited) < len(handling_request):
                    ite+=1
                    # print('cccccccccccccc', len(visited) + len(assigned), len(handling_request))
                    probability = self.dyn_generate_probability(current_node, candidate_list, visited, remain_capacity, solution_time,time)
                    
                    # print("COMPARE")
                    # self.print_route([candidate_list])
                    # print(*visited)
                    # print("COMPARE")

                    # print("SOLUTION")
                    # self.print_route(solution)
                    # print("SOLUTION")

                    
                    if len(probability) == 0:  # Check capacity constraint for vehicle
                        #solution[pointer].append(self.depot)
                        pointer += 1
                        #solution[pointer].append([self.depot])
                        if pointer >= len(solution):
                            solution.append([self.depot])
                            solution_time = time
                        else:
                            route_time = 0
                            for j in range(1, len(solution[pointer])):
                                route_time += self.network.links[(solution[pointer][j-1].node,solution[pointer][j].node)].distance
                                route_time = max(route_time, solution[pointer][j].start)
                            solution_time = route_time

                        current_node = solution[pointer][-1]
                        remain_capacity = self.max_capacity - sum(i.demand for i in solution[pointer])
                        # print('run here')

                        # if feasible == False:
                        #     break
                        # feasible = False

                        continue

                    feasible = True

                    next_node = self.choose_next_node(probability)
                    
                    # print("capa ", remain_capacity)
                    # print(next_node.node)
                    

                    solution[pointer].append(next_node)
                    visited.add(next_node.node)

                    # print('ket o day')
                    # self.print_route(solution)
                    remain_capacity -= next_node.demand

                    solution_time += self.network.links[(current_node.node, next_node.node)].distance
                    solution_time = max(solution_time, next_node.start) #neu den som thi doi

                    if remain_capacity < 0:  # Check capacity constraint for vehicle
                        solution[pointer].pop()
                        visited.remove(next_node.node)
                        # solution[pointer].append(self.depot)
                        pointer += 1
                        # solution.append([self.depot])
                        if pointer >= len(solution):
                            solution.append([self.depot])
                            solution_time = time
                        else:
                            route_time = 0
                            for j in range(1, len(solution[pointer])):
                                route_time += self.network.links[(solution[pointer][j-1].node,solution[pointer][j].node)].distance
                                route_time = max(route_time, solution[pointer][j].start)
                            solution_time = route_time


                        current_node = solution[pointer][-1]
                        remain_capacity = self.max_capacity - sum(i.demand for i in solution[pointer])
        
                        continue

                    current_node = next_node

                if feasible: solutions.append(solution)


            self.update_pheromone(solutions)

            self.best_distance = float('inf')
            self.best_solution = None
            
            for solution in solutions:
                distance = self.calculate_solution_distance(solution)
                # print(distance)
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_solution = solution
            
            #tu coming route toi uu, sua planning route
            self.planning_route = copy.deepcopy(self.best_solution)
            print("SOLUTION")
            self.print_route(self.best_solution)
            print("SOLUTION")

            #check condition to update present_route
            for i in range(len(self.planning_route)):
                if i >= len(self.present_route): #them duong moi theo planning route
                    self.present_route.append([self.depot,self.planning_route[i][1]])
                    for request in handling_request:
                        if request.node == self.planning_route[i][1].node:
                            handling_request.remove(request)
                else:
                    route_time = 0
                    for j in range(1, len(self.planning_route[i])):
                        route_time += self.network.links[(self.planning_route[i][j-1].node,self.planning_route[i][j].node)].distance
                        route_time = max(route_time, self.planning_route[i][j].start)
                        # if (self.planning_route[i][j] not in self.present_route[i]):

                        cd = True
                        for node in self.present_route[i]: #neu da nam trong present_route roi thi khong xu li
                            if node.node == self.planning_route[i][j].node: cd = False
                        
                        if (route_time < time+timestep) and cd:
                            self.present_route[i].append(self.planning_route[i][j])
                            print("ASSIGN TO ROUTE: ", i, " NODE ", self.planning_route[i][j].node)
                            for request in handling_request:
                                if request.node == self.planning_route[i][j].node:
                                    handling_request.remove(request)


            print("TIMESTEP: ", time)
            print("PRESENT")
            self.print_route(self.present_route)
            print(self.calculate_solution_distance(self.present_route))
            print("PRESENT")
            print("PLANNING")
            self.print_route(self.planning_route)
            print(self.calculate_solution_distance(self.planning_route))
            print("PLANNING")
            print("HANDLING")
            print(len(handling_request))
            self.print_route([handling_request])
            print("HANDLING")
        
            time += timestep

        for route in self.present_route:
            route.append(self.depot)
        print("FINAL")
        self.print_route(self.present_route)
        print(self.calculate_solution_distance(self.present_route))
        print("FINAL")

    def dyn_generate_probability(self, current_node, candidate_list, visited, remain_capacity, solution_time, timetime):
        probability = list()
        total = 0
        # print(current_node.node)
        for request in candidate_list: 
            if request.node not in visited:
                # if remain_capacity >= request.demand:
                if solution_time + self.network.links[(current_node.node, request.node)].distance < request.end:
                    if solution_time + self.network.links[(current_node.node, request.node)].distance >= request.start:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)].distance)**self.beta  #cong thuc toan hoc cua haco
                        probability.append((request,total))
                    else:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)].distance 
                                                                                                 + request.end - (self.network.links[(current_node.node,request.node)].distance + solution_time))**self.beta  #doi request bat dau
                        probability.append((request,total))
                # else: print("bbbbbbb", request.node, solution_time + self.network.links[(current_node.node, request.node)].distance, request.start, request.end, timetime)
                    # print(total)
            # else: print("aaaaaaaaaa")

        probability = [(node, prob / total) for node, prob in probability]
        return probability
    

    def generate_probability(self, current_node, candidate_list, visited, remain_capacity, solution_time):
        probability = list()
        total = 0
        for request in candidate_list: 
            if request.node not in visited:
                # if remain_capacity >= request.demand:
                if solution_time + self.network.links[(current_node.node, request.node)].distance < request.end:
                    if solution_time + self.network.links[(current_node.node, request.node)].distance >= request.start:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)].distance)**self.beta  #cong thuc toan hoc cua haco
                        probability.append((request,total))
                    else:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)].distance 
                                                                                                 + request.end - (self.network.links[(current_node.node,request.node)].distance + solution_time))**self.beta  #doi request bat dau
                        probability.append((request,total))

        probability = [(node, prob / total) for node, prob in probability]
        return probability
    
    def choose_next_node(self, probability):
        r = np.random.rand()
        for node, prob in probability:
            if r <= prob:
                return node


    def generate_pheromone(self):
        self.pheromone = np.ones((self.network.num_nodes, self.network.num_nodes))

    def update_pheromone(self, solutions):
        delta_pheromone = np.zeros_like(self.pheromone)
        for solution in solutions:
            for i in range(len(solution)):
                for j in range(len(solution[i])-1):
                    current_node = solution[i][j]
                    next_node = solution[i][j+1]
                    delta_pheromone[current_node.node][next_node.node] += self.q / self.calculate_solution_distance(solution)

        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone

        # self.pheromone =  (self.pheromone + delta_pheromone)

    def calculate_solution_distance(self, solution):
        if self.check_capacity(solution, self.max_capacity) and self.check_time(solution): return float('inf')
        distance = 0
        for i in range(len(solution)):
            for j in range(len(solution[i])-1):
                distance += self.network.links[(solution[i][j].node,solution[i][j+1].node)].distance
        return distance
    
    
    def check_capacity(self, route: list, max_capacity):
        #check capacity
        for i in range(len(route)):
            cap = 0
            for request in route[i]:
                # print(request)
                cap += request.demand
            if cap > max_capacity:
                return False
        return True
        
    def check_time(self, route: list):
        #check time window
        time = 0
        for i in range(len(route)):
            for j in range(len(route[i])-1):
                time = time + 0 + self.network.links[(route[i][j].node, route[i][j+1].node)].distance
                if time < route[i][j+1].start:
                    time = route[i][j+1].start
                if time > route[i][j+1].end:
                    return False
        return True
    
    def print_route(self, route):
        #lam 1 function rieng
        for i in range(len(route)):
            for j in range(len(route[i])):
                print(route[i][j].node, end = ' ')
            print()


if __name__ == "__main__":
    np.random.seed(1)
    problem1 = ProblemTD("data/VRPTWD/VRPTWD-instance-112.xlsx")
    haco = TD_DACO(problem1)