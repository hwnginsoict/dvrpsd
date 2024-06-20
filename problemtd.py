from graph import Node
from graph import Request
from graph import Network
import numpy as np


class ProblemTD:
    def __init__(self, instance):
        with open(instance, 'r') as f:
            all = f.readlines()
        customers = {}
        request = []
        self.num_vehicle = None
        self.capacity = None
        self.network = None
        self.dynamic_prob = 0.25
        self.seed = 21
        np.random.seed(self.seed)

        for i in range(len(all)): #nhap du lieu, tao file cac request, customer
            if all[i] == 'NUMBER     CAPACITY\n':
                self.num_vehicle, self.capacity = map(int,all[i+1].strip().split())
            if all[i] == 'CUSTOMER\n':

                while (i+3)<len(all):
                    num, x, y, demand, s, e, w = map(float,all[i+3].strip().split())

                    rand = np.random.random()   #set 25% request la static (time = 0)
                    if rand < self.dynamic_prob:
                        time = 0
                    else:
                        time = np.random.random() * s #set time bang random(0,s), distribution = random, uniform

                    rand = np.random.random()
                    drone_serve = 1
                    if rand < 0.5:
                        drove_serve = 0

                    req = Request(node = int(num), demand = demand, start = s, end = e, time = time, drone_serve = drone_serve)
                    request.append(req) 

                    cus = Node(id = int(num), x = x, y = y)
                    customers[int(num)] = cus
                    i = i+1
                break
        # self.depot = request.pop(0) #bo depot ra khoi request

        self.requests = sorted(request, key=lambda x: x.time)
        self.network = Network(customers)

        
if __name__ == "__main__": #nay de test thoi
    np.random.seed(1)
    problem1 = ProblemTD("data/C100/C101.TXT")
    k=0
    for i in problem1.requests:
        print(i.node, i.time)
        