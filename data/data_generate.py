import numpy as np
import pandas as pd
from graph import *
from vehicle import *
import os


class DataGenerate:
    def __init__(self, kind, instance):
        if kind == 'solomon':
            self.generate_data_solomon(instance)
        if kind == 'easy':
            raise Exception
            self.generate_data_easy(instance)

    def generate_data_solomon(self, instance):
        with open(instance, 'r') as f:
            all = f.readlines()
        self.customers = {}
        request = []
        self.num_vehicle = None
        self.capacity = None
        self.network = None
        self.dynamic_prob = 0.10
        self.seed = 21
        np.random.seed(self.seed)

        for i in range(len(all)): #nhap du lieu, tao file cac request, customer
            if all[i] == 'NUMBER     CAPACITY\n':
                self.num_vehicle, self.capacity = map(int, all[i+1].strip().split())
            if all[i] == 'CUSTOMER\n':

                while (i+3) < len(all):
                    num, x, y, demand, s, e, w = map(float, all[i+3].strip().split())

                    x = 50/60*x
                    y = 50/60*y

                    w = 5

                    drone_cap = 10
                    truck_cap = 1300

                    if e < 60:
                        time = 0
                    else:
                        rand = np.random.random()  # set ?% request as static (time = 0)
                        if rand < self.dynamic_prob:
                            time = 0
                        else:
                            time = max(np.random.random() * (s - 60), 0)  # set time as random(0,s), distribution = random, uniform

                    if demand > drone_cap:
                        drone_serve = 0
                    else:
                        drone_serve = 1
                        rand = np.random.random()
                        if rand < 0.25:
                            drone_serve = 0


                    req = Request(node=int(num), demand=demand, start=s, end=e, servicetime=w, time=time, drone_serve=drone_serve)
                    request.append(req)

                    cus = Node(id=int(num), x=x, y=y)
                    self.customers[int(num)] = cus
                    i = i + 1
                break

        self.requests = sorted(request, key=lambda x: x.time)

    def generate_data_easy(self, instance):
        self.customers = {}
        request = []
        self.num_vehicle = None

        self.network = None
        self.dynamic_prob = 0.25
        self.seed = 21
        np.random.seed(self.seed)

        df = pd.read_excel(instance, sheet_name=None)
        customer_data = df["Sheet1"].iloc[0:]

        for num, row in customer_data.iterrows():
            x, y, demand, s, e, w = row

            rand = np.random.random()  # set 25% request as static (time = 0)
            if rand < self.dynamic_prob:
                time = float(0)
            else:
                time = np.random.random() * s  # set time as random(0,s), distribution = random, uniform

            rand = np.random.random()

            drone_serve = 0
            if rand < 0.3:  # set probability of customer being served by drone
                drone_serve = 0
            # if  #set if drone can visit that 

            req = Request(node=int(num), demand=demand, start=s, end=e, time=time, drone_serve=drone_serve)
            request.append(req)

            cus = Node(id=int(num), x=x, y=y)
            self.customers[int(num)] = cus

        self.requests = sorted(request, key=lambda x: x.time)

    def export_to_csv(self, folder, filename):
        # Ensure the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(folder, filename)

        data = []
        for req in self.requests:
            data.append({
                'x': self.customers[req.node].x,
                'y': self.customers[req.node].y,
                'demand': req.demand,
                'open': req.start,
                'close': req.end,
                'servicetime': req.servicetime,
                'drone_serve': req.drone_serve,
                'time': req.time,
            })

        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)


# Example usage
# data_gen = DataGenerate(kind='solomon', instance='path_to_instance_file')
# data_gen.export_to_csv('output.csv')

list = [
    'c101', 'c102', 'c103', 'c104', 'c105', 'c106', 'c107', 'c108', 'c109',
    'c201', 'c202', 'c203', 'c204', 'c205', 'c206', 'c207', 'c208',
    'r101', 'r102', 'r103', 'r104', 'r105', 'r106', 'r107', 'r108', 'r109', 'r110', 'r111', 'r112',
    'r201', 'r202', 'r203', 'r204', 'r205', 'r206', 'r207', 'r208', 'r209', 'r210', 'r211',
    'rc101', 'rc102', 'rc103', 'rc104', 'rc105', 'rc106', 'rc107', 'rc108',
    'rc201', 'rc202', 'rc203', 'rc204', 'rc205', 'rc206', 'rc207', 'rc208'
]
 

# for i in list:
#     data_gen = DataGenerate(kind='solomon', instance= str('F:\\CodingEnvironment\\dvrpsd\\data\\Solomon\\C100\\' + i + '.txt'))
#     data_gen.export_to_csv('F:\CodingEnvironment\dvrpsd\data\dvrptw', str('h100' + i + '.csv'))


list_name = ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']
for name in list_name:
    for i in range(1,11):
        data_gen = DataGenerate(kind='solomon', instance= str('F:\\CodingEnvironment\\dvrpsd\\data\\Solomon\\1000\\' + name + '_10_' + str(i) + '.TXT'))
        data_gen.export_to_csv('F:\\CodingEnvironment\\dvrpsd\\data\\dvrptw\\1000', str('h1000' + name + '_10_' + str(i) + '.csv'))



# def generate_filenames_and_export(idx):
#     instance=f'F:\\CodingEnvironment\\dvrpsd\\data\\VRPTWD\\VRPTWD-instance-{idx}.xlsx'
#     data_gen = DataGenerate(kind='easy', instance=instance)

#     # Read the Excel file to get the number of customers
#     df = pd.read_excel(instance, sheet_name=None)
#     customer_data = df["Sheet1"].iloc[0:]
#     num_customers = len(customer_data) - 1
#     # print(num_customers)

#     # Generate the filename
#     name_file = f'e{num_customers}r1{idx}.csv'

#     # Export the data to CSV
#     data_gen.export_to_csv('data/dvrptw', name_file)



# for i in range(1,113):
#     generate_filenames_and_export(i)


