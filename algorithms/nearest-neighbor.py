import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from graph.network import Network
from graph.node import Node
from problem import Problem
from problemtd import ProblemTD
from algorithms.ls.search2 import Search2
from algorithms.ls.search1 import Search1
from algorithms.insertion import Insertion
import random
import copy

class HACO:
    def __init__(self, network, requests, max_capacity):
        self.network = network
        self.split_requests(requests)
        self.max_capacity = max_capacity
        self.set_parameter()
        self.generate_pheromone()
        self.static_routing()
        self.dynamic_routing(40)

    def set_parameter(self):
        self.num_ants = 50
        self.max_iteration_static = 3
        self.max_iteration_dynamic = 10
        self.alpha = 1
        self.beta = 2
        self.rho = 0.6
        self.q = 100
        self.best_distance = float('inf')
        self.best_solution = None

    def split_requests(self, requests):
        self.sta_requests = list()
        self.dyn_requests = list()
        for request in requests:
            if request.time == 0:
                self.sta_requests.append(request)
            else:
                self.dyn_requests.append(request)

    def static_routing(self):
        for i in range(self.max_iteration_static):
            solutions = list()
            candidate_list = list()
            for request in self.sta_requests:
                candidate_list.append(request)
            self.depot = candidate_list.pop(0)
            print("hello this is", self.depot.node)
            for ant in range(self.num_ants):
                solution = [[self.depot]]
                pointer = 0
                remain_capacity = self.max_capacity
                visited = set()
                solution_time = 0
                current_node = self.depot
                while len(visited) < len(self.sta_requests) - 1:
                    probability = self.generate_probability(current_node, candidate_list, visited, remain_capacity, solution_time)
                    if len(probability) == 0:
                        solution[pointer].append(self.depot)
                        pointer += 1
                        solution.append([self.depot])
                        current_node = self.depot
                        remain_capacity = self.max_capacity
                        solution_time = 0
                        continue
                    next_node = self.choose_next_node(probability)
                    solution[pointer].append(next_node)
                    visited.add(next_node.node)
                    remain_capacity -= next_node.demand
                    solution_time += self.network.links[(current_node.node, next_node.node)] 
                    solution_time = max(solution_time, next_node.start)
                    if remain_capacity < 0:
                        solution[pointer].pop()
                        solution[pointer].append(self.depot)
                        pointer += 1
                        solution.append([self.depot])
                        current_node = self.depot
                        remain_capacity = self.max_capacity
                        solution_time = 0
                        continue
                    current_node = next_node
                if solution[pointer] == [self.depot]:
                    solution.pop()
                else:
                    solution[pointer].append(self.depot)
                solutions.append(solution)
            self.update_pheromone(solutions)
            for solution in solutions:
                distance = self.calculate_solution_distance(solution)
                print(distance)
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_solution = solution
            print("Best: ", self.best_distance)
            self.print_route(self.best_solution)

    def dynamic_routing(self, timestep):
        print("DYNAMICC")
        timestep = 50
        time = self.depot.start
        coming_requests = self.dyn_requests
        handling_requests = []
        all_requests = []
        self.routes = sorted(self.best_solution, key=len)
        while time < self.depot.end:
            for request in list(coming_requests):
                if request.time <= time:
                    handling_requests.append(request)
                    all_requests.append(request)
                    coming_requests.remove(request)
                else:
                    break
            while handling_requests:
                print('take request')
                request = handling_requests.pop(0)
                best_route = None
                best_position = None
                best_increase = float('inf')
                for route in self.routes:
                    for i in range(1, len(route)):
                        new_route = route[:i] + [request] + route[i:]
                        if self.check_capacity([new_route], self.max_capacity) and self.check_time([new_route]):
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
                    self.routes.insert(0, [self.depot, request, self.depot])
            self.print_route(self.routes)
            print(f"Distance: {self.calculate_solution_distance(self.routes)}")
            time += timestep
            print(f"Time: {time}, Handling Requests Left: {len(handling_requests)}")
        self.print_route(self.routes)
        print(f"Final Distance: {self.calculate_solution_distance(self.routes)}")

    def generate_probability(self, current_node, candidate_list, visited, remain_capacity, solution_time):
        probability = list()
        total = 0
        for request in candidate_list:
            if request.node not in visited:
                if solution_time + self.network.links[(current_node.node, request.node)]  < request.end:
                    if solution_time + self.network.links[(current_node.node, request.node)]  >= request.start:
                        total += (self.pheromone[(current_node.node, request.node)] ** self.alpha) / (
                                    self.network.links[(current_node.node, request.node)] )
                        probability.append((request, total))
                    else:
                        total += (self.pheromone[(current_node.node, request.node)] ** self.alpha) / (
                                    self.network.links[(current_node.node, request.node)] 
                                    + request.end - (
                                                self.network.links[(current_node.node, request.node)]  + solution_time))
                        probability.append((request, total))
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
                for j in range(len(solution[i]) - 1):
                    current_node = solution[i][j]
                    next_node = solution[i][j + 1]
                    delta_pheromone[current_node.node][next_node.node] += self.q / self.calculate_solution_distance(solution)
        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone

    def calculate_solution_distance(self, solution):
        if not (self.check_capacity(solution, self.max_capacity) or self.check_time(solution)): return float('inf')
        distance = 0
        for i in range(len(solution)):
            for j in range(len(solution[i]) - 1):
                distance += self.network.links[(solution[i][j].node, solution[i][j + 1].node)] 
        return distance

    def check_capacity(self, route: list, max_capacity):
        for i in range(len(route)):
            cap = 0
            for request in route[i]:
                cap += request.demand
            if cap > max_capacity:
                return False
        return True

    def check_time(self, route: list):
        time = 0
        for i in range(len(route)):
            for j in range(len(route[i]) - 1):
                time = time + 0 + self.network.links[(route[i][j].node, route[i][j + 1].node)] 
                if time < route[i][j + 1].start:
                    time = route[i][j + 1].start
                if time > route[i][j + 1].end:
                    return False
        return True

    def print_route(self, route):
        for i in range(len(route)):
            for j in range(len(route[i])):
                print(route[i][j].node, end=' ')
            print()

if __name__ == "__main__":
    seed = 1
    np.random.seed(seed)
    problem1 = ProblemTD("F:\\CodingEnvironment\\dvrpsd\\data\\dvrptw\\100\\h100c101.csv")
    network = problem1.network
    requests = problem1.requests
    max_capacity = problem1.truck.capacity
    haco = HACO(network=network, requests=requests, max_capacity=max_capacity)
