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
        self.problem = problem
        self.network = problem.network
        self.split_requests(problem.requests)
        self.max_capacity = problem.truck.capacity

        self.cotacdung = 0

        self.set_parameter()
        self.generate_pheromone()
        
        self.static_routing()

        print("DONE STATIC")

        self.dynamic_routing(40)



        print("co tac dung", self.cotacdung)
        
        

    def set_parameter(self):
        self.num_ants_static = 10  #100
        self.max_iteration_static = 10   #100

        self.num_ants_dynamic = 50 #100
        self.max_iteration_dynamic = 10 #50

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
        for i in range (self.max_iteration_static):
            solutions = list()
            candidate_list = list()
            for request in self.sta_requests:
                candidate_list.append(request)

            self.depot = candidate_list.pop(0)   #bo depot ra khoi candidate list

            # print("hello this is", self.depot.node)

            for ant in range(self.num_ants_static):
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

                    solution_time += self.network.links[(current_node.node, next_node.node)]/self.problem.truck.velocity
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

                else: solution[pointer].append(self.depot)  # Return to depot


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
            
            print("Best: ", self.best_distance)
            self.print_routeTD(self.best_solution)
    
    def dynamic_routing(self, timestep):
        # timestep = 20
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

        #cho xe di luon
        for i in range(len(self.planning_route)):
            self.present_route.append([self.depot,self.planning_route[i][1]])
            # self.present_route.insert(0,[self.depot,self.planning_route[i][1]])
            for request in handling_request:
                if request.node == self.planning_route[i][1].node:
                    handling_request.remove(request)

        self.check_drone = [0 for i in range(len(self.present_route))] #create list to check if route have drone

        assigned = [0]

        self.handling_heuristics = copy.deepcopy(handling_request)
        
        while (time < self.depot.end):

            temp_heuristics = []

            for route in self.present_route:
                for request in route:
                    if request.node not in assigned:
                        assigned.append(request.node)

            for route in self.present_route:
                if len(route) == 1:
                    self.present_route.remove(route)

            print("FIRST PRESENT")
            self.print_routeTD(self.present_route)
            print(self.calculate_solution_distance(self.present_route))
            print("FIRST PRESENT")
            print("ASSIGNED: ", assigned)

            for i in self.dyn_requests:
                if i.node == 0: continue 
                if i.time < time and (i not in handling_request) and (i.node not in assigned):
                    handling_request.append(i)
                    all_request.append(i)

                    # print("HANDLING")
                    # for request in handling_request:
                    #     print(request.node, end =" ")
                    # print()
                    # print("HANDLING")

                    if i in coming_request:
                        coming_request.remove(i)

                    if i not in self.handling_heuristics:
                        self.handling_heuristics.append(i)
                        temp_heuristics.append(i)

            #self.planning heuristic de tan dung tri thuc tu truoc
            # """
            # self.handling_heuristics 

            handling = copy.deepcopy(temp_heuristics)
            heuristic_route = copy.deepcopy(self.planning_route)
            while handling:
                request = handling.pop(0)
                best_route = None
                best_position = None
                best_increase = float('inf')
                for route in heuristic_route:
                    for i in range(1, len(route)):
                        if route[i].node in assigned:
                            continue
                        else:
                            new_route = route[:i] + [request] + route[i:]
                            if self.check_capacity([new_route], self.max_capacity) and self.check_timeTD([new_route]):
                                increase = (self.network.links[(route[i - 1].node, request.node)]  +
                                            self.network.links[(request.node, route[i].node)]  -
                                            self.network.links[(route[i - 1].node, route[i].node)] )
                                if increase < best_increase:
                                    best_route = route
                                    best_position = i
                                    best_increase = increase
                if best_route is not None:
                    best_route.insert(best_position, request)
                else:
                    heuristic_route.insert(0, [self.depot, request, self.depot])

            if not self.check_timeTD(heuristic_route): 
                raise Exception
            
            print("HEURISTIC")
            self.print_routeTD(heuristic_route)
            print("HEURISTIC")

            for route in heuristic_route:

                if route[-1].node == 0:
                    route.pop()
                if len(route) == 0:
                    heuristic_route.remove(route)

            print("HEURISTIC")
            self.print_routeTD(heuristic_route)
            print("HEURISTIC")

        
            self.drone_routing(heuristic_route)
            self.best_solution = heuristic_route
            self.best_distance = self.calculate_solution_distance(heuristic_route)
            if self.best_distance == float('inf'): raise Exception

            print("PLANNING")
            self.print_routeTD(self.planning_route)
            print(self.calculate_solution_distance(self.planning_route))
            print("PLANNING")

            # """

            
            # xu li dinh tuyen lai bang ACO, xu li tren coming_route
            if time % 80 == 0: 
            # if True:
                self.generate_pheromone()
                self.update_pheromone([self.best_solution])

                for m in range(self.max_iteration_dynamic): 
                    for ants in range(self.num_ants_dynamic):
                        random.shuffle(self.present_route)

                        solution = copy.deepcopy(self.present_route)
                        pointer = 0
                        remain_capacity = sum(i.demand for i in solution[0])
                        visited = set()
                        current_node = self.present_route[0][-1]

                        if self.present_route[0][-1].node == 0:
                            solution_time = time
                        else: 
                            route_time = 0
                            for j in range(1, len(self.present_route[pointer])):
                                # print(pointer, j)
                                # print(self.planning_route[pointer][j-1].node,self.planning_route[pointer][j].node)
                                route_time += self.network.links[(self.present_route[0][j-1].node,self.present_route[0][j].node)]/self.problem.truck.velocity #@lam o day, tach truck va drone ra
                                route_time = max(route_time, self.present_route[0][j].start)
                            solution_time = route_time

                        candidate_list = copy.deepcopy(handling_request)
                        solutions = []
                    

                        ite=1
                        feasible = True
                        count = 0
                        while len(visited) < len(handling_request):
                            ite+=1
                            probability = self.dyn_generate_probability(current_node, candidate_list, visited, remain_capacity, solution_time,time)
                            
                            if len(probability) == 0:  # Check capacity constraint for vehicle
                                #solution[pointer].append(self.depot)
                                pointer += 1
                                #solution[pointer].append([self.depot])
                                if pointer >= len(solution):
                                    solution.append([self.depot])
                                    solution_time = time

                                    if feasible == False and count > 20:
                                        # solution = None
                                        solution = solution[:-22]
                                        break
                                    feasible = False
                                    count += 1
                                else:
                                    route_time = 0
                                    for j in range(1, len(solution[pointer])):
                                        route_time += self.network.links[(solution[pointer][j-1].node,solution[pointer][j].node)] 
                                        route_time = max(route_time, solution[pointer][j].start)
                                    solution_time = route_time

                                    count = 0
                                    feasible = True

                                current_node = solution[pointer][-1]
                                remain_capacity = self.max_capacity - sum(i.demand for i in solution[pointer])
                                # print('run here')

                                # if feasible == False:
                                #     solution = None
                                #     break
                                # feasible = False
                                continue

                            count = 0
                            feasible = True
                            next_node = self.choose_next_node(probability)
            
                            solution[pointer].append(next_node)
                            visited.add(next_node.node)
                            remain_capacity -= next_node.demand

                            solution_time += self.network.links[(current_node.node, next_node.node)] /self.problem.truck.velocity
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
                                        route_time += self.network.links[(solution[pointer][j-1].node,solution[pointer][j].node)] / self.problem.truck.velocity
                                        route_time = max(route_time, solution[pointer][j].start)
                                    solution_time = route_time


                                current_node = solution[pointer][-1]
                                remain_capacity = self.max_capacity - sum(i.demand for i in solution[pointer])
                
                                continue

                            current_node = next_node

                        # rand = random.random()
                        # if rand < 0.5:
                            # self.drone_routing(solution)
                        
                        self.drone_routing_all(solution)

                        solutions.append(solution)


                    self.update_pheromone(solutions)

                    # self.best_distance = float('inf')
                    # self.best_solution = None
                    
                    for solution in solutions:
                        distance = self.calculate_solution_distance(solution)
                        # print(distance)
                        if distance < self.best_distance:
                            self.best_distance = distance
                            self.best_solution = solution

                            self.cotacdung += 1
                            self.update_pheromone([solution])
            
            #tu coming route toi uu, sua planning route
            self.planning_route = copy.deepcopy(self.best_solution)
            print("SOLUTION")
            self.print_routeTD(self.best_solution)
            print("SOLUTION")

            #check condition to update present_route
            '''
            for i in range(len(self.planning_route)):
                if i >= len(self.present_route): #them duong moi theo planning route
                    self.present_route.append([self.depot,self.planning_route[i][1]])

                    self.check_drone.append(0)

                    for request in handling_request:
                        if request.node == self.planning_route[i][1].node:
                            handling_request.remove(request)
                else:
                    route_time = 0
                    for j in range(1, len(self.planning_route[i])):
                        route_time += self.network.links[(self.planning_route[i][j-1].node,self.planning_route[i][j].node)] 
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

            '''

            self.present_route = []
            for i in range(len(self.planning_route)):
                self.present_route.append([self.depot])
                check_time1 = 0
                for j in range(1, len(self.planning_route[i])):
                    check_time1 += self.network.links[(self.planning_route[i][j-1].node,self.planning_route[i][j].node)] 
                    check_time1 = max(route_time, self.planning_route[i][j].start)
                    if (check_time1 < time+timestep) or (self.planning_route[i][j].node in assigned) :
                        self.present_route[i].append(self.planning_route[i][j])
                        for request in handling_request:
                            if request.node == self.planning_route[i][j].node:
                                handling_request.remove(request)

                        if self.planning_route[i][j].node not in assigned:
                            assigned.append(self.planning_route[i][j].node)
                    






            print("TIMESTEP: ", time)
            print("PRESENT")
            self.print_routeTD(self.present_route)
            print(self.calculate_solution_distance(self.present_route))
            print("PRESENT")
            print("PLANNING")
            self.print_routeTD(self.planning_route)
            print(self.calculate_solution_distance(self.planning_route))
            print("PLANNING")

            print("HANDLING")
            print(len(handling_request))
            self.print_route([handling_request])
            print("HANDLING")


            # rand = random.random()
            # if rand < 0.5:
            #     self.drone_routing_present()

        
            time += timestep

        for route in self.present_route:
            route.append(self.depot)
        print("FINAL")
        self.print_routeTD(self.present_route)
        print(self.calculate_solution_distance(self.present_route))
        print("FINAL")

        self.result = (self.calculate_carbon_emission(self.present_route), (100 - self.count_request(self.present_route)))

    def dyn_generate_probability(self, current_node, candidate_list, visited, remain_capacity, solution_time, timetime):
        probability = list()
        total = 0
        # print(current_node.node)
        for request in candidate_list: 
            if request.node not in visited:
                # if remain_capacity >= request.demand:
                pheromone = self.pheromone[(current_node.node,request.node)]
                distance = self.network.links[(current_node.node,request.node)]/self.problem.truck.velocity
                waiting = max(request.end - (self.network.links[(current_node.node,request.node)]/self.problem.truck.velocity  + solution_time) , 0)
                td_diff = 1

                '''
                if solution_time + self.network.links[(current_node.node, request.node)]  < request.end:
                    if solution_time + self.network.links[(current_node.node, request.node)]  >= request.start:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)] )**self.beta  #cong thuc toan hoc cua haco
                        probability.append((request,total))
                    else:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)]  
                                                                                                 + request.end - (self.network.links[(current_node.node,request.node)]  + solution_time))**self.beta  #doi request bat dau
                        probability.append((request,total))
                '''

                if solution_time + self.network.links[(current_node.node, request.node)]/self.problem.truck.velocity  < request.end:
                    total += (pheromone)**self.alpha * (1/distance)**self.beta * (1/waiting) * (1/td_diff)
                    probability.append((request, total))


        probability = [(node, prob / total) for node, prob in probability]
        return probability
    

    def drone_routing_present(self):

        all_list = []
        for i in range(len(self.planning_route)):
            # if self.check_drone[i] == 1:
            #     all_list.append(None)
            #     continue
            list = self.planning_route[i][len(self.present_route[i]) - 1 :]  #CAREFUL CONSIDER here present = [1,2,3], planning = [1,2,3,4,5,6,7], list = [3,4,5,6,7]
            all_list.append(list)

        for i in range(len(all_list)):
            # if self.check_drone[i] == 0:
            if True:
                route = all_list[i]
                temp = self.drone_choose_node(route)
                if temp == False:
                    continue
                else:
                    [drone_node, index] = temp
                    # route[index].to_drone()
                    # raise Exception
                    for j in range(len(self.present_route[i]) - 1, len(self.planning_route[i])): #check can than xem co loi o phan -1, lay index khong
                        if self.planning_route[i][j].node == drone_node.node:
                            self.planning_route[i][j].to_drone()
                            # raise Exception
                            
    def drone_routing(self, solution):

        if solution == None: return

        for i in range(len(solution)):
            route = solution[i]

            # cd = False
            # for request in route:
            #     if request.service_type == 'drone':
            #         cd = True
            # if cd: continue
                    
                
            temp = self.drone_choose_node(route)

            if temp == False:
                continue
            else:
                [drone_node, index] = temp
                # route[index].to_drone()
                # raise Exception
                for j in range(len(solution[i])): 
                    if solution[i][j].node == drone_node.node:
                        solution[i][j].to_drone()
                        # raise Exception

        
                        

    def drone_choose_node(self, list):
        remain = self.problem.drone.endure
        cap = self.problem.drone.capacity

        list_compare = []
        
        for i in range(1, len(list)):
            if i != len(list)-1:
                obj = float('inf')
                if list[i].demand < cap:
                    # print(list[i-1].node, list[i].node, list[i+1].node)
                    drone_time = self.network.links[(list[i-1].node, list[i].node)]  + self.network.links[(list[i].node, list[i+1].node)]  / self.problem.drone.velocity
                    truck_time = self.network.links[(list[i-1].node, list[i+1].node)]  / self.problem.truck.velocity
                    obj = abs(truck_time - drone_time)
                    if drone_time > self.problem.drone.endure: 
                        obj = float('inf')
                list_compare.append([obj, i])
            else:
                obj = float('inf')
                if list[i].demand < cap:
                    # print(list[i-1].node, list[i].node)
                    drone_time = self.network.links[(list[i-1].node, list[i].node)]  + self.network.links[(list[i].node, 0)]  / self.problem.drone.velocity
                    if list[i-1].node != 0:    
                        truck_time = self.network.links[(list[i-1].node, 0)]  / self.problem.truck.velocity
                    else: 
                        truck_time = 0
                    obj = abs(truck_time - drone_time)
                    if drone_time > self.problem.drone.endure: 
                        obj = float('inf')
                list_compare.append([obj,i])
        
        list_compare.sort(key=lambda x: x[0])

        if len(list_compare) > 0:
            obj , index = list_compare[0]
            if obj != float('inf'):
                drone_node = list[index]
                return [drone_node, index]
        return False
    
    def drone_routing_all(self, solution):
        for route in solution:
            self.drone_choose_all(route)
    
    def drone_choose_all(self, list):
        remain = self.problem.drone.endure
        cap = self.problem.drone.capacity

        for i in range(1, len(list)):
            if i != len(list)-1:
                if list[i].demand < cap and list[i-1].service_type == 'truck':
                    drone_time = self.network.links[(list[i-1].node, list[i].node)]  + self.network.links[(list[i].node, list[i+1].node)]  / self.problem.drone.velocity
                    truck_time = self.network.links[(list[i-1].node, list[i+1].node)]  / self.problem.truck.velocity
                    if drone_time < self.problem.drone.endure: 
                        list[i].to_drone()
                
            elif list[i].node != 0:
                if list[i].demand < cap and list[i-1].service_type == 'truck':
                    drone_time = self.network.links[(list[i-1].node, list[i].node)]  + self.network.links[(list[i].node, 0)]  / self.problem.drone.velocity
                    if list[i-1].node != 0:    
                        truck_time = self.network.links[(list[i-1].node, 0)]  / self.problem.truck.velocity
                    else: 
                        truck_time = 0
                    if drone_time < self.problem.drone.endure: 
                        list[i].to_drone()


    def generate_probability(self, current_node, candidate_list, visited, remain_capacity, solution_time):
        probability = list()
        total = 0
        for request in candidate_list: 
            if request.node not in visited:
                # if remain_capacity >= request.demand:
                if solution_time + self.network.links[(current_node.node, request.node)]/self.problem.truck.velocity  < request.end:
                    if solution_time + self.network.links[(current_node.node, request.node)]/self.problem.truck.velocity  >= request.start:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)] )**self.beta  #cong thuc toan hoc cua haco
                        probability.append((request,total))
                    else:
                        total += (self.pheromone[(current_node.node,request.node)]**self.alpha)/(self.network.links[(current_node.node,request.node)]  
                                                                                                 + request.end - (self.network.links[(current_node.node,request.node)]/self.problem.truck.velocity  + solution_time))**self.beta  #doi request bat dau
                        probability.append((request,total))

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
            for i in range(len(solution)):
                for j in range(len(solution[i])-1):
                    current_node = solution[i][j]
                    next_node = solution[i][j+1]
                    delta_pheromone[current_node.node][next_node.node] += self.q / self.calculate_solution_distance(solution)

        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone

        # self.pheromone =  (self.pheromone + delta_pheromone)

    # def calculate_solution_distance(self, solution):

    #     if (solution == None): return float('inf')
    #     if not (self.check_capacity(solution, self.max_capacity) or self.check_time(solution)): return float('inf') #du ma no ac
    #     distance = 0
    #     for i in range(len(solution)):
    #         for j in range(len(solution[i])-1):
    #             # print(solution[i][j].node, solution[i][j+1].node)
    #             distance += self.network.links[(solution[i][j].node,solution[i][j+1].node)] 
    #     return distance

    
    def calculate_carbon_emission(self, solution): #version 1, only 1 drone for the route
        if not (self.check_capacity(solution, self.max_capacity)): 
            # print("BUG")
            # self.print_routeTD(solution)
            # raise Exception
            return float('inf')
        if not (self.check_timeTD(solution)): 
            # print("BUG")
            # self.print_routeTD(solution)
            raise Exception
            return float('inf')
        # carbon_emission = 0
        truck_length= 0
        drone_length = 0
        truck_route = []
        drone_route = []
        for route in solution:
            # if len(route) == 1: continue
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
    
    def calculate_solution_distance(self, solution):
        return self.calculate_carbon_emission(solution) + len(solution)*00 + (self.network.num_nodes -1 - self.count_request(solution)) * 500
    
    
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
            time = 0
            for j in range(len(route[i])-1):
                time = time + 0 + self.network.links[(route[i][j].node, route[i][j+1].node)]/self.problem.truck.velocity
                if time < route[i][j+1].start:
                    time = route[i][j+1].start
                if time > route[i][j+1].end:
                    return False
        return True
    
    def check_timeTD(self, route: list):
        time = 0
        for i in range(len(route)):
            time = 0
            for j in range(1, len(route[i])):
                if route[i][j].service_type == 'drone':
                    continue
                else:
                    if route[i][j-1].service_type == 'truck':
                        time = time + 0 + self.network.links[(route[i][j-1].node, route[i][j].node)] / self.problem.truck.velocity
                        if time < route[i][j].start:
                            time = route[i][j].start
                        if time > route[i][j].end:
                            return False
                    else:
                        time_truck = time + 0 + self.network.links[(route[i][j-2].node, route[i][j].node)] / self.problem.truck.velocity
                        if time_truck > route[i][j].end:
                            return False
                        time_drone = time + 0 + (self.network.links[(route[i][j-2].node, route[i][j-1].node)] + self.network.links[(route[i][j-1].node, route[i][j].node)])/self.problem.drone.velocity
                        time = max(time_truck, time_drone)

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
        print("Emmission: " , self.calculate_carbon_emission(route))
    def count_request(self, solution):
        count = 0
        for route in solution:
            count += len(route) - 2
        return count
            
if __name__ == "__main__":
    np.random.seed(3)
    problem1 = ProblemTD("F:\\CodingEnvironment\\dvrpsd\\data\\dvrptw\\100\\h100r101.csv")
    # problem1 = ProblemTD("F:\\CodingEnvironment\\dvrpsd\\data\\dvrptw\\1000\\h1000C1_10_1.csv")
    haco = TD_DACO(problem1)
    print(haco.result)