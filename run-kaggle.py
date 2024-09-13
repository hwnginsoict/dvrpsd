# Import necessary libraries
from algorithms.infer import INFER
from problemtd import ProblemTD

import csv
import os
import numpy as np

# Define the input directory where the CSV files are stored in the Kaggle environment
input_dir = '/kaggle/input/dvrptw/dvrptw/100/'  # Change this to the correct dataset path in Kaggle

# List of files to process
file_list = ['h100r101.csv', 'h100r102.csv', 'h100r103.csv', 'h100r104.csv', 'h100r105.csv', 
             'h100r106.csv', 'h100r107.csv', 'h100r108.csv', 'h100r109.csv', 'h100r110.csv', 
             'h100r111.csv', 'h100r112.csv']

# Output file path
output_file_path = '/kaggle/working/new_final_csv.csv'

# Ensure the file is created and write the header if it doesn't exist
if not os.path.exists(output_file_path):
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file_name', 'seed', 'td', 'rd'])  # Add seed column to the header

# Loop over the seed values and file names
for file_name in file_list:
    for seed in range(1, 11):
        np.random.seed(seed)  # Set the seed

        # Load the problem using the correct path for Kaggle
        problem1 = ProblemTD(os.path.join(input_dir, file_name))
        
        # Initialize and run the INFER algorithm
        haco = INFER(problem1)
        result = haco.result  # Get the result

        # Append the seed to the result and write it to the CSV file immediately
        with open(output_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([file_name, seed, result[0], result[1]])  # Include seed in the result

print("Results have been written to", output_file_path)
