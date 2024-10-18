from algorithms.inferv1 import INFERV1
from algorithms.td_daco import TD_DACO
from problemtd import ProblemTD
import csv
import os
import numpy as np
import time  # Add this to track time

# List of files
# file_list = [ 'h100c201.csv', 'h100rc101.csv', 'h100rc201.csv']
file_list = ['h100c101.csv']

# Ensure the file is created and write the header
file_path = 'collected1.csv'
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
                problem1 = ProblemTD("F:/CodingEnvironment/dvrpsd/data/dvrptw/100/" + file_name)
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
                    writer.writerow([file_name, seed,nista,nidyn, result[0], result[1], running_time])  # Include seed in the result

# End time measurement
# end_time = time.time()
# running_time = end_time - start_time

# Print the running time
# print(f"Results have been written to {file_path} in {running_time:.2f} seconds.")
