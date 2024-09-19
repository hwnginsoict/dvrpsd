from algorithms.inferv1 import INFERV1
from problemtd import ProblemTD

import csv
import os
import numpy as np

# List of files
# file_list = ['h100c101.csv', 'h100c102.csv', 'h100c103.csv', 'h100c104.csv', 'h100c105.csv', 'h100c106.csv', 'h100c107.csv', 'h100c108.csv', 'h100c109.csv', 
#              'h100c201.csv', 'h100c202.csv', 'h100c203.csv', 'h100c204.csv', 'h100c205.csv', 'h100c206.csv', 'h100c207.csv', 'h100c208.csv', 
#              'h100r101.csv', 'h100r102.csv', 'h100r103.csv', 'h100r104.csv', 'h100r105.csv', 'h100r106.csv', 'h100r107.csv', 'h100r108.csv', 'h100r109.csv', 'h100r110.csv', 'h100r111.csv', 'h100r112.csv', 
#              'h100r201.csv', 'h100r202.csv', 'h100r203.csv', 'h100r204.csv', 'h100r205.csv', 'h100r206.csv', 'h100r207.csv', 'h100r208.csv', 'h100r209.csv', 'h100r210.csv', 'h100r211.csv', 
#              'h100rc101.csv', 'h100rc102.csv', 'h100rc103.csv', 'h100rc104.csv', 'h100rc105.csv', 'h100rc106.csv', 'h100rc107.csv', 'h100rc108.csv', 
#              'h100rc201.csv', 'h100rc202.csv', 'h100rc203.csv', 'h100rc204.csv', 'h100rc205.csv', 'h100rc206.csv', 'h100rc207.csv', 'h100rc208.csv']

# file_list = ['h100r101.csv', 'h100r102.csv', 'h100r103.csv', 'h100r104.csv', 'h100r105.csv', 'h100r106.csv', 'h100r107.csv', 
#              'h100r108.csv', 'h100r109.csv', 'h100r110.csv', 'h100r111.csv', 'h100r112.csv']

file_list = ['h100c104.csv']

# Ensure the file is created and write the header
file_path = 'new_final_csv_local.csv'
if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file_name', 'seed', 'td', 'rd'])  # Add seed column to the header

# Loop over the seed values
for file_name in file_list:

    for seed in range(1, 3):
        np.random.seed(seed)  # Set the seed

        problem1 = ProblemTD("F:/CodingEnvironment/dvrpsd/data/dvrptw/100/" + file_name)
        haco = INFERV1(problem1)
        result = haco.result  # Get the result

        # Append the seed to the result and write it to the file immediately
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([file_name, seed, result[0], result[1]])  # Include seed in the result

print("Results have been written to", file_path)
