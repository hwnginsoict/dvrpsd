import numpy as np

from graph.network import Network

from problem import Problem

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
        self.max_iteration = 100

        self.alpha = 1
        self.beta = 2
        self.rho = 0.5
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
            candidate_list.pop(0)   #bo depot ra khoi candidate list

            for ant in range(self.num_ants):
                solution = [0] #start from depot
                remain_capacity = self.max_capacity
                visited = set()

                current_node = 0

                while len(visited) < len(self.sta_requests) -1:  # Visit all customers
                    probability = self.generate_probability(current_node, candidate_list, visited, remain_capacity)
                    next_node = self.choose_next_node(probability)

                    # print("capa ", remain_capacity)
                    # print(next_node.node)

                    solution.append(next_node.node)
                    visited.add(next_node.node)
                    remain_capacity -= next_node.demand

                    if remain_capacity < 0:  # Check capacity constraint for vehicle
                        solution.pop()
                        solution.append(0)
                        current_node = 0
                        remain_capacity = self.max_capacity
                        continue

                    current_node = next_node.node

                    # print(solution)


                solution.append(0)  # Return to depot
                solutions.append(solution)
            
            self.update_pheromone(solutions)
        
            for solution in solutions:
                    distance = self.calculate_solution_distance(solution)
                    if distance < self.best_distance:
                        self.best_distance = distance
                        self.best_solution = solution

            # self.best_solution = best_solution
            # self.best_distance = best_distance

            print(i, self.best_solution, self.best_distance)


    def generate_probability(self, current_node, candidate_list, visited, remain_capacity):
        probability = list()
        total = 0
        for request in candidate_list: 
            if request.node not in visited:
                # if remain_capacity >= request.demand:
                    total += (self.pheromone[(current_node,request.node)]**self.alpha)*(self.network.links[(current_node,request.node)].distance)  #cong thuc toan hoc cua haco
                    probability.append((request,total))

        probability = [(node, prob / total) for node, prob in probability]
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
                delta_pheromone[current_node][next_node] += self.q / self.calculate_solution_distance(solution)

        self.pheromone = (1 - self.rho) * self.pheromone + delta_pheromone

    def calculate_solution_distance(self, solution):
        distance = 0
        for i in range(len(solution)-1):
            distance += self.network.links[(solution[i],solution[i + 1])].distance
        return distance


if __name__ == "__main__":
    np.random.seed(1)
    problem1 = Problem("data/C200/C1_2_1.TXT")
    network = problem1.network
    requests = problem1.requests
    max_capacity = problem1.capacity
    haco = HACO(network = network, requests = requests, max_capacity = max_capacity)


