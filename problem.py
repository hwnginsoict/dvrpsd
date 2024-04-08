from graph import Node
from graph import Request
import numpy as np


class Problem:
    def __init__(self, instance):
        with open("data/C1_2_1.TXT", 'r') as f:
            all = f.readlines()
        self.customer = {}
        self.request = np.array([])
        for line in all:
            if line == 'NUMBER     CAPACITY\n':
                num_vehicle, cap = map(int,line.strip().split())
            
        