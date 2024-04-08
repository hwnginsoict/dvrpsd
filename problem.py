from graph import Node
from graph import Request
import numpy as np


class Problem:
    def __init__(self, instance):
        with open(instance, 'r') as f:
            all = f.readlines()
        self.customer = {}
        self.request = []
        for i in range(len(all)):
            if all[i] == 'NUMBER     CAPACITY\n':
                self.num_vehicle, self.capacity = map(int,all[i+1].strip().split())
            if all[i] == 'CUSTOMER\n':
                while (i+3)<len(all):
                    num, x, y, demand, s, e, w = map(float,all[i+3].strip().split())
                    print(num, x,y, demand)
                    request = Request(int(num), demand, s, e, None)
                    self.request.append(request)

                    print(request.demand)

                    customer = Node(int(num), x, y)
                    self.customer[int(num)] = customer
                    i = i+1
                break
            
if __name__ == "__main__":
    problem1 = Problem("data/C200/C1_2_1.TXT")
    for node_id, node in problem1.customer.items():
        print(node.x, node.y, node.id)