from graph import Node
from graph import Request
from graph import Network
from vehicle import Truck, Drone
import numpy as np
import pandas as pd


class ProblemTD:
    def __init__(self, instance):
        

        customers = {}
        request = []
        self.num_vehicle = None
        self.capacity = None
        self.network = None
        self.dynamic_prob = 0.25
        self.seed = 21
        np.random.seed(self.seed)

        df = pd.read_excel(instance, sheet_name=None)
        customer_data = df["Sheet1"].iloc[0:]
        # print(customer_data.iterrows())

        for num, row in customer_data.iterrows():
            x, y, demand, s, e, w = row
            # print(x, y, demand, s, e, w)

            rand = np.random.random()  # set 25% request as static (time = 0)
            if rand < self.dynamic_prob:
                time = 0
            else:
                time = np.random.random() * s  # set time as random(0,s), distribution = random, uniform

            rand = np.random.random()
            drone_serve = 0
            if rand < 0.3:  # set probability of customer being served by drone
                drone_serve = 0

            req = Request(node=int(num), demand=demand, start=s, end=e, time=time, drone_serve=drone_serve)
            request.append(req)

            cus = Node(id=int(num), x=x, y=y)
            customers[int(num)] = cus

        self.requests = sorted(request, key=lambda x: x.time)
        # for i in self.requests:
        #     print(i.node, i.time)
        self.network = Network(customers)
        self.truck = Truck(35, 100)
        self.drone = Drone(50, 5)

        
if __name__ == "__main__": #nay de test thoi
    np.random.seed(1)
    problem1 = ProblemTD("data/VRPTWD/VRPTWD-instance-112.xlsx")
    for i in problem1.requests:
        print(i.node, i.time)

        