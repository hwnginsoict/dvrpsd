# Import necessary libraries
from algorithms.inferv1 import INFERV1
from algorithms.td_daco import TD_DACO
from problemtd import ProblemTD

import csv
import os
import numpy as np
import time

# Define the input directory where the CSV files are stored in the Kaggle environment
input_dir = '/kaggle/input/dvrptw/dvrptw/100/'  # Change this to the correct dataset path in Kaggle

# List of files to process
# file_list = ['h100r201.csv', 'h100r202.csv', 'h100r203.csv', 'h100r204.csv', 'h100r205.csv', 'h100r206.csv']
             
# file_list =  ['h100rc101.csv', 'h100rc102.csv', 'h100rc103.csv', 'h100rc104.csv', 'h100rc105.csv', 'h100rc106.csv', 'h100rc107.csv', 'h100rc108.csv', 'h100rc201.csv', 'h100rc202.csv', 'h100rc203.csv', 'h100rc204.csv', 'h100rc205.csv', 'h100rc206.csv', 'h100rc207.csv', 'h100rc208.csv']

# file_list = ['h100c201.csv', 'h100c202.csv', 'h100c203.csv', 'h100c204.csv']

# file_list = ['h100c205.csv', 'h100c206.csv', 'h100c207.csv', 'h100c208.csv']

file_list = [ 'h100c201.csv', 'h100rc101.csv', 'h100rc201.csv']

# Output file path
output_file_path = '/kaggle/working/new_final_csv_latest.csv'

file_path = 'finetune_static.csv'
if not os.path.exists(file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file_name', 'seed', 'ni sta', 'ni dyn', 'td', 'rd', 'time'])  # Add seed column to the header

# Start measuring time
# start_time = time.time()

# Loop over the seed values and files
for file_name in file_list:
    for seed in [1,2,3]:
        for nista in [10,20,50,100]:
            for nidyn in [5,10,20,30]:
                np.random.seed(seed)  # Set the seed

                # Solve the problem and get the result
                problem1 = ProblemTD("/kaggle/input/dvrptw/dvrptw/100/" + file_name)
                start_time = time.time()
                haco = TD_DACO(problem1)

                haco.num_ants_static = nista
                haco.max_iteration_static = nista
                haco.num_ants_dynamic = nidyn
                haco.max_iteration_dynamic = nidyn

                haco.run()

                end_time = time.time()
                result = haco.result  # Get the result
                running_time = end_time - start_time


                # Write results to the CSV file
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([file_name, seed, nista,nidyn, result[0], result[1], running_time])  # Include seed in the result


print("Results have been written to", output_file_path)
