from graph import Node
from graph import Request
from graph import Network
import numpy as np


class Problem:
    def __init__(self, instance):
        with open(instance, 'r') as f:
            all = f.readlines()
        customers = {}
        request = []
        self.num_vehicle = None
        self.capacity = None
        self.network = None
        self.dynamic_prob = 0.10
        self.seed = 21
        np.random.seed(self.seed)

        for i in range(len(all)): #nhap du lieu, tao file cac request, customer
            if all[i] == 'NUMBER     CAPACITY\n':
                self.num_vehicle, self.capacity = map(int,all[i+1].strip().split())
            if all[i] == 'CUSTOMER\n':

                while (i+3)<len(all):
                    num, x, y, demand, s, e, w = map(float,all[i+3].strip().split())
                
                    if e < 60:
                        time = 0
                    
                    else:
                        rand = np.random.random()   #set 25% request la static (time = 0)
                        if rand < self.dynamic_prob:
                            time = 0
                        else:
                            time = max(np.random.random() * (s-60),0) #set time bang random(0,s), distribution = random, uniform

                    req = Request(node = int(num), demand = demand, start = s, end = e, time = time)
                    request.append(req) 

                    cus = Node(id = int(num), x = x, y = y)
                    customers[int(num)] = cus
                    i = i+1
                break
        # request.remove(request[0]) #bo depot ra khoi request

        self.requests = sorted(request, key=lambda x: x.time)
        self.network = Network(customers)

        
if __name__ == "__main__": #nay de test thoi
    np.random.seed(1)
    problem1 = Problem("data/C100/c101.TXT")
    count = 0
    for i in problem1.requests:
        print(i.node, i.time, i.start, i.end)
        if i.time ==0: count += 1
    print(1-count/len(problem1.requests))
        