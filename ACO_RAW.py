import matplotlib.pyplot as plt
import numpy as np
import math
import random
import copy

class Ant:
    def __init__(self,data,capacity,q0):
        self.data=data
        self.travel=()
        self.capacity=capacity
        self.time_window={}
        self.pheromon={}
        self.current_point=1
        self.q0=q0
        self.cordination=[]
        self.distance_matrix={}
        self.next_node=1
        self.intensity={}
        self.time_window={}
        self.alpha=1
        self.beta=2
        self.gama=1
        self.theta = 0.75
        self.visited_list=[1]
        self.candidate_list=[]
        self.probability_q0={}
        self.probability_q={}
        self.probability_q_norm={}
        self.minimum_capacity=0
        self.capcities={}
        self.travel_distance=0
        self.rho=0.6
        self.pheromon_numbers={}
        self.Q=1
        self.service_time=0.00
        self.serv_list=[]
        self.f = 2
        self.g = 2
        self.rho_local = 1

    def customer_cord(self):
        for i in range(len(self.data)):
            cords=[float(self.data[i][1]),float(self.data[i][2])]
            self.cordination.append(cords)
        return self.cordination
    
    def euclidean_distance(self):
        for i in range(len(self.cordination)):
            for j in range(len(self.cordination)):
                distance=math.sqrt(((self.cordination[i][0]-self.cordination[j][0])**2)+((self.cordination[i][1]-self.cordination[j][1])**2))
                self.distance_matrix[i+1,j+1]=distance
                try:
                    self.intensity[i+1,j+1]=1/distance
                except:
                    self.intensity[i+1,j+1]=-99999999
        return self.distance_matrix,self.intensity
    

    def width_window(self):    
        for i in self.data:
            self.time_window[i[0]]=float(i[5])-float(i[4])
        return self.time_window
    
    def path_pheromon(self):
        for node_i in self.data:
            for node_j in self.data:
                self.pheromon[int(node_i[0]),int(node_j[0])]=1
        return self.pheromon
    

    def make_candidate_list(self):
        self.candidate_list=[]
        for node in self.data:
            if int(node[0]) not in self.visited_list:
                self.candidate_list.append(int(node[0]))
        return self.candidate_list
    


    def choose_next_node(self):
        if len(self.candidate_list)==0:
            self.next_node=1
            return self.next_node
        elif len(self.candidate_list)==1:
            
            self.next_node=self.candidate_list[0]
            if float(self.data[int(self.next_node) - 1][3])<self.capacity and self.service_time + float(self.distance_matrix[self.current_point, self.next_node]) <= float(self.data[self.next_node - 1][5]):
                
                return self.next_node
            else:
                self.next_node=1
                return self.next_node
                
        else:
            next_node=0
            self.probability_q0={}
            self.probability_q={}
            self.probability_q_norm={}
            for node in self.candidate_list:
                w = 1
                if self.service_time + float(self.distance_matrix[self.current_point,node]) < float(self.data[node - 1][4]):
                    w = float(self.data[node - 1][4]) - (self.service_time + float(self.distance_matrix[self.current_point,node]))

                saving = float(self.distance_matrix[self.current_point,1]) + float(self.distance_matrix[1,node]) - self.g * float(self.distance_matrix[self.current_point,node]) + self.f * np.abs(float(self.distance_matrix[self.current_point,1]) - float(self.distance_matrix[1,node]))


                self.probability_q0[self.current_point,node]=(self.pheromon[self.current_point,node]**self.alpha)*(self.intensity[self.current_point,node]**self.beta)*((saving**self.gama)) * ((1/w)**self.theta)
            for node in self.candidate_list:
                w = 1
                if self.service_time + float(self.distance_matrix[self.current_point,node]) < float(self.data[node - 1][4]):
                    w = float(self.data[node - 1][4]) - (self.service_time + float(self.distance_matrix[self.current_point,node]))
                saving = float(self.distance_matrix[self.current_point,1]) + float(self.distance_matrix[1,node]) - self.g * float(self.distance_matrix[self.current_point,node]) + self.f * np.abs(float(self.distance_matrix[self.current_point,1]) - float(self.distance_matrix[1,node]))

                self.probability_q[self.current_point,node]=(self.pheromon[self.current_point,node]**self.alpha)*(self.intensity[self.current_point,node]**self.beta)*((saving**self.gama)) * ((1/w)**self.theta)/ max(self.probability_q0.values())

            def softmax_normalize(dictionary):
                values = np.array(list(dictionary.values()), dtype=np.float64)
                exp_values = np.exp(values - np.max(values)) 
                normalized_values = exp_values / np.sum(exp_values)
                normalized_dict = dict(zip(dictionary.keys(), normalized_values))
                return normalized_dict
            
            
            self.probability_q_norm =softmax_normalize(self.probability_q)
            self.capcities={}
            for node in self.candidate_list:
                self.capcities[node]=float(self.data[node-1][3])
            q=random.random()
            self.next_node = None

            if q<=self.q0:

                sorted_value_q0=sorted(self.probability_q0.values(),reverse=True)
                for i in range(len(sorted_value_q0)):
                    for key,value in self.probability_q0.items():
                        if value==sorted_value_q0[i]:
                            if float(self.data[key[1]-1][3])<=self.capacity and self.service_time+ float(self.distance_matrix[key[1], key[0]]) <=float(self.data[key[1]-1][5]) :
                                next_node=key[1]
                                self.next_node=next_node
                                return self.next_node
  
            else:
                def roulette_wheel_selection(values, probabilities):
                    selected_key = random.choices(list(values), weights=list(probabilities), k=1)[0]
                    return selected_key
                for item in self.probability_q_norm:
                    selected_key = roulette_wheel_selection(self.probability_q_norm.keys(), self.probability_q_norm.values())
                    if float(self.data[selected_key[1]-1][3])<=self.capacity and self.service_time+ float(self.distance_matrix[selected_key[1], selected_key[0]])<=float(self.data[selected_key[1] - 1][5]):
                        next_node=selected_key[1]
                        self.next_node=next_node
                        return self.next_node
                    else:
                        continue
                self.next_node=None
                return self.next_node
            return self.next_node
            
    
    def move(self):
        if self.next_node==None:
            self.next_node=1
            self.travel=(self.current_point,1)
        else:
            self.visited_list.append(self.next_node)
            self.travel=(self.current_point,self.next_node)
            if self.service_time + self.distance_matrix[self.travel[0], self.travel[1]] < float(self.data[self.travel[1]-1][4]):
                self.service_time=float(self.data[self.travel[1]-1][4])+float(self.data[self.travel[1]-1][6])
            else:
                self.service_time += float(self.distance_matrix[self.travel[0], self.travel[1]]) + float(self.data[self.travel[1]-1][6])

            self.serv_list.append(self.service_time)
            self.capacity=self.capacity-float(self.data[self.next_node-1][3])
            self.current_point=self.next_node
        
        self.travel_distance+=self.distance_matrix[self.travel]

        return self.travel
    
    def update_rho(self):
        self.rho=0.9*self.rho
        return self.rho
    
    def update_rho_local(self):
        self.rho=1.5*self.rho_local
        return self.rho_local
    

    def update_pheromon(self,ants_travels, distance):
        for travel in ants_travels:
            self.pheromon[travel] = self.pheromon[travel] * (1-self.rho) + 1/distance
        return self.pheromon
    
    def update_global(self, ants_travels, distance):
        for travel in ants_travels:
            # self.pheromon[travel]=self.pheromon[travel] * (1-self.rho) + 1/distance
            self.pheromon[travel] += 1/distance
        return self.pheromon
    
    def update_local_search(self, ants_travels, distance):
        for travel in ants_travels:
            # self.pheromon[travel]=self.pheromon[travel] * (1-self.rho) + 1/distance
            self.pheromon[travel] += 1/distance
        return self.pheromon

def check_feasible(customer, route, colony):
    m = len(route)
    for i in range(1,m):
        service_time = 0
        CAPACITY = colony.capacity 
        new_route = route.copy()
        new_route.insert(i, customer)
        cnt = 0
        for j in range(m):
            
            if (float(colony.data[new_route[j+1] - 1][3])) <= CAPACITY and (service_time + float(colony.distance_matrix[new_route[j], new_route[j+1]]) <= float(colony.data[new_route[j+1] - 1][5])):
                cnt += 1
                CAPACITY -= float(colony.data[new_route[j+1] - 1][3])
                if service_time + float(colony.distance_matrix[new_route[j], new_route[j+1]]) < float(colony.data[new_route[j+1] - 1][4]):
                    service_time = float(colony.data[new_route[j+1] - 1][4]) + float(colony.data[new_route[j+1]-1][6])
                else:
                    service_time += float(colony.distance_matrix[new_route[j], new_route[j+1]]) + float(colony.data[new_route[j+1]-1][6])
            else:
                break
        if cnt == m:
            return new_route 
    return []

def local_search(selected_route, ants_route, colony, index):
     ants_route_new = ants_route.copy()
     selected_route_new = selected_route.copy()
     for customer in selected_route[1:-1]:
          for i, route in enumerate(ants_route_new.values()):
               if i != index:
                    new_route = check_feasible(customer, route, colony)
                    if new_route != []:
                        ants_route_new[i] = new_route
                        selected_route_new.remove(customer)
                        break
     ants_route_new[index] = selected_route_new
     travel_distance = 0
     for route in ants_route_new.values():
          for i in range(len(route)-1):
               travel_distance += colony.distance_matrix[route[i], route[i+1]]
     if travel_distance < colony.travel_distance:
          # print("OK")
          return travel_distance, ants_route_new
     return colony.travel_distance, ants_route


def split_route(ants_route):
     result = []
     for route in ants_route.values():
          for i in range(len(route)-1):
               result.append((route[i], route[i+1]))
     return result

def check(route):
    route2 = copy.deepcopy(route)

    # check cap
    cap = 0 
    for x in route2:
        cap += demand[x]
    if cap>max_cap: 
        return False
    
    #check time
    cur_time=0
    for i in range(len(route2)-1):
        cur_time=cur_time+s_time[route2[i]]+distance(route2[i],route2[i+1])
        if cur_time<e_time[route[i+1]]:
            cur_time=e_time[route2[i+1]]
        if cur_time>l_time[route2[i+1]]:
            return False
    return True

def distance(i,j): #tính khoảng cách 2 điểm
    return ((xcoord[i]-xcoord[j])**2+(ycoord[i]-ycoord[j])**2)**(1/2)

def cost2(route):  # tính tổng đường đi của 1 cá thể
    if route[0]!=-1:
        sum=0
        for i in route:
            for j in range(0,len(i)-1):
                sum+=distance(int(i[j]),int(i[j+1]))
        return sum
    else:
        return float('inf')
def route_1(routes):
    route=copy.deepcopy(routes)
    for i in range(len(route)):
        for j in range(len(route[i])):
            route[i][j]-=1
    return route

def route__1(routes):
    route=copy.deepcopy(routes)
    for i in range(len(route)):
        for j in range(len(route[i])):
            route[i][j]+=1
    return route

def search(route):
    route=route_1(route)
    for i in range(len(route)-1):
        for j in range(i+1,len(route)):
            for k in range(1,len(route[i])-1):
                for t in range(1,len(route[j])-1):
                        new_route=copy.deepcopy(route)
                        z=new_route[i][k]
                        new_route[i][k]=new_route[j][t]
                        new_route[j][t]=z
                        if check(new_route[i]) and check(new_route[j]) and cost2(new_route)< cost2(route):
                            z=route[i][k]
                            route[i][k]=route[j][t]
                            route[j][t]=z
    return route__1(route)

def search2(routes):
    routes=route_1(routes)
    while routes[-1]==[0,0]:
        routes.pop()
    for i in range(len(routes)):
        for j in range(len(routes)):
            if i!=j:
                k=1
                while (k<len(routes[i])-1):
                    for t in range(1,len(routes[j])-1):
                      if k<len(routes[i])-1:
                        new_route=copy.deepcopy(routes)
                        z=new_route[i][k]
                        new_route[i].pop(k)
                        new_route[j].insert(t,z)
                        if cost2(new_route)< cost2(routes) and check(new_route[j]):
                            routes[i].pop(k)
                            routes[j].insert(t,z)
                        
                    k+=1
    return route__1(routes)

def search4(route):
    route=route_1(route)
    for i in range(len(route)-1):
        for j in range(i+1,len(route)):
            for k1 in range(1,len(route[i])-2):
              for k2 in range(k1+1,len(route[i])-1):
                for t1 in range(1,len(route[j])-2):
                  for t2 in range(t1+1,len(route[j])-1):
                        new_route=copy.deepcopy(route)
                        zk=copy.deepcopy(new_route[i][k1:k2+1])
                        zt=copy.deepcopy(new_route[j][t1:t2+1])
                        del new_route[i][k1:k2+1]
                        del new_route[j][t1:t2+1]
                        new_route[i]=new_route[i][:k1]+zt+new_route[i][k1:]
                        new_route[j]=new_route[j][:t1]+zk+new_route[j][t1:]
                        if cost2(new_route)< cost2(route) and check(new_route[i]) and check(new_route[j]):
                            zk=copy.deepcopy(route[i][k1:k2+1])
                            zt=copy.deepcopy(route[j][t1:t2+1])
                            del route[i][k1:k2+1]
                            del route[j][t1:t2+1]
                            route[i]=route[i][:k1]+zt+route[i][k1:]
                            route[j]=route[j][:t1]+zk+route[j][t1:]
                            return route__1(route)
                            
    return route__1(route)

def local_search2(t):
    t1=copy.deepcopy(t)
    routes=[]
    for i in range(len(t1)):
        routes.append(t1[i])

    
    
    routes=search4(search2(search(routes)))
    
    index=0
    result={}
    for x in (routes):
        if x!=[1,1]:
            result[index]=x
            index+=1
    return cost2((route_1(routes))),result

xcoord=np.array([])
ycoord=np.array([])
demand=np.array([])
e_time=np.array([])
l_time=np.array([])
s_time=np.array([])

data = open('F:\\CodingEnvironment\\dvrpsd\\data\Solomon\\C100\\C104.txt','r')
lines = data.readlines()
for i in range(len(lines)):
    if lines[i]=='NUMBER     CAPACITY\n':
        veh_num,max_cap=map(int,lines[i+1].strip().split())
    if lines[i]=='CUSTOMER\n':
        j=i+3
        while j<len(lines):
            a,b,c,d,e,f,g=map(int,lines[j].strip().split())
            xcoord=np.append(xcoord,b)
            ycoord=np.append(ycoord,c)
            demand=np.append(demand,d)
            e_time=np.append(e_time,e)
            l_time=np.append(l_time,f)
            s_time=np.append(s_time,g)
            j+=1
cus_num=len(demand)-1
veh_num=100

data=[]
for i in range(1,cus_num+2):
    new_data=[str(i)]
    new_data.append(str(int(xcoord[i-1])))
    new_data.append(str(int(ycoord[i-1])))
    new_data.append(str(int(demand[i-1])))
    new_data.append(str(int(e_time[i-1])))
    new_data.append(str(int(l_time[i-1])))
    new_data.append(str(int(s_time[i-1])))
    data.append(new_data)

max_cap = 1300
CAP=max_cap
colony=Ant(data,CAP,0.9)
colony.customer_cord()
colony.euclidean_distance()
colony.width_window()
colony.path_pheromon()
result = 10000

max_iteration = 100
k=0
current_best = float('inf')
for k in range(max_iteration):
    # current_best = 10000
    final = []
    final_travel = []
    for j in range(100):
        min_path = 100
        index = 999
    
        colony.travel_distance = 0
        # print(k, "----", j)
        ants_travels={}
        ants_route={}
        travels=[]
        travels_2 = []
        path=[1]
        i=0
        colony.visited_list = [1]
        while True:
            colony.make_candidate_list()
            colony.choose_next_node()
            colony.move()
            path.append(colony.next_node)
            travel=colony.travel
            travels.append(travel)
            if travel[1]==1:
                if travel==(1,1):
                    break
                else:
                    ants_travels[i]=travels
                    # colony.update_pheromon(ants_travels[i])
                    ants_route[i]=path
                    if len(path) < min_path:
                        min_path = len(path)
                        index = i
                        
                    path=[1]
                    travels=[]
                    i=i+1
                    colony.current_point=1
                    colony.capacity=CAP
                    colony.service_time=0
            travel=colony.travel
            travels_2.append(travel)
        

        travel_distance, ants_route = local_search(ants_route[index].copy(), ants_route.copy(), colony, index)
        colony.travel_distance = travel_distance
        travels_2 = split_route(ants_route)
       
        
        if colony.travel_distance < result:
            result = colony.travel_distance
            best_ant_travel = travels_2
            final_route = ants_route
            travel_distance_1, ants_route_1 = local_search2(ants_route)
            if travel_distance_1 < result:
                print('Update')
                result = travel_distance_1
                final_route = ants_route_1
                best_ant_travel = split_route(ants_route_1)
                travels_2 = best_ant_travel
                colony.travel_distance = result 
            print(result)

        if colony.travel_distance < current_best:
            current_best = colony.travel_distance
            print('best: ', current_best)
            current_best_route = travels_2
        final.append(travels_2)
        final_travel.append(colony.travel_distance)
        
    colony.update_rho()
    for h, l in enumerate(final):  
        colony.update_pheromon(l, final_travel[h])
    colony.update_global(current_best_route, current_best)
    print('Done {}'.format(k))