import pandas as pd

def read_VRPTW(filename):
    data = pd.read_excel(filename)
    print(data)

read_VRPTW("F:\CodingEnvironment\dvrpsd\data\VRPTWD\VRPTWD-instance-8.xlsx")