# Import necessary libraries
from algorithms.inferv1 import INFERV1
# from algorithms.td_daco import 
from algorithms.inferv2 import INFER_V2
from problemtd import ProblemTD

import csv
import os
import numpy as np
import time
import copy


n = 4

# Define the input directory where the CSV files are stored in the Kaggle environment
input_dir = '/kaggle/working/dvrpsd/data/dvrptw/' + str(n) + '00/'  # Change this to the correct dataset path in Kaggle

# List of files to process
# file_list = ['h100r201.csv', 'h100r202.csv', 'h100r203.csv', 'h100r204.csv', 'h100r205.csv', 'h100r206.csv']
             
# file_list =  ['h100rc101.csv', 'h100rc102.csv', 'h100rc103.csv', 'h100rc104.csv', 'h100rc105.csv', 'h100rc106.csv', 'h100rc107.csv', 'h100rc108.csv', 'h100rc201.csv', 'h100rc202.csv', 'h100rc203.csv', 'h100rc204.csv', 'h100rc205.csv', 'h100rc206.csv', 'h100rc207.csv', 'h100rc208.csv']

# file_list = ['h100c201.csv', 'h100c202.csv', 'h100c203.csv', 'h100c204.csv']

# file_list = ['h100c205.csv', 'h100c206.csv', 'h100c207.csv', 'h100c208.csv']

# file_list = [ 'h100c201.csv', 'h100rc101.csv', 'h100rc201.csv']

# Output file path
file_path = '/kaggle/working/dvrpsd/compare_params.csv'
if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file_name', 'seed', 'ited', 'sized', 'td', 'rd', 'time'])  # Add seed column to the header

# Start measuring time
# start_time = time.time()

# Loop over the seed values and files


for type in ['C1']:#, 'R1', 'RC1', 'C2', 'R2', 'RC2']:
    for n in [4]:
        for i in [2]:
            input_dir = '/kaggle/working/dvrpsd/data/dvrptw/' + str(n) + '00/'
            file_name = 'h' + str(n) + '00' + type + '_' + str(n) +'_' + str(i) + '.csv'
            problem1 = ProblemTD(input_dir + file_name)
            haco = INFER_V2(problem1)

            haco.num_ants_static = 50
            haco.max_iteration_static = 50
            haco.run_static()

            for ited in [30]:
                for sized in [10,20,30]:

                    for seed in range(1,4):
                        haco_temp = copy.deepcopy(haco)

                        np.random.seed(seed)  # Set the seed 

                        # Solve the problem and get the result
                        haco_temp.num_ants_dynamic = sized
                        haco_temp.max_iteration_dynamic = ited
                        start_time = time.time()

                        haco_temp.run_dynamic()

                        end_time = time.time()
                        result = haco_temp.result  # Get the result
                        running_time = end_time - start_time


                        # Write results to the CSV file
                        with open(file_path, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([file_name, seed, ited, sized, result[0], result[1], running_time])  # Include seed in the result
                            print(file_name, seed, ited, sized, result[0], result[1], running_time)

print("Results have been written to", file_path)
