import csv
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

def calculate_risk(directory_path):
    # Constants
    constant_for_saf = 55  # Modify as needed
    threshold = 35
    threshold_forgiveness = 0.5

    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))
    rps = []
    i=1
    for csv_file in csv_files:
        ml, mf, tl, tf = 0, 0, 0, 0
        threshold_boolean = True

        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Type'] in ['Import', 'Import ... from ...']:
                    ml += int(row['Weight'])
                    tl += 1
                    if(int(row['Weight']) >= threshold):
                        threshold_boolean = False 
                elif 'function' in row['Type'].lower():
                    mf += int(row['Weight'])
                    tf += 1
                    tl += 1
                    if(int(row['Weight']) >= threshold):
                        threshold_boolean = False 

        # Calculate SAF (Scale Adjustment Factor)
        if (threshold_boolean == True):
            ml = ml * threshold_forgiveness
            mf = mf * threshold_forgiveness
        saf = 1 + (constant_for_saf / (tl if tl > 0 else 1))

        # Calculate Risk Percentage (RP)
        rp = ((ml + mf) / (tf if tf > 0 else 1)) * saf
        if rp > 100:
            rp = 100
     
        rps.append(rp)
        print(f"{i}: {os.path.basename(csv_file)} RP: {rp:.2f}%")
        i = i+1
        #print(f"Risk analysis for {os.path.basename(csv_file)}:")
        #print(f"  ML (Malicious Libraries): {ml}")
        #print(f"  MF (Malicious Functions): {mf}")
        #print(f"  TL (Total Lines): {tl}")
        #print(f"  TF (Total Functions): {tf}")
        #print(f"  SAF (Scale Adjustment Factor): {saf:.2f}")
        #print(f"  RP (Risk Percentage): {rp:.2f}%")
        #print(f"  Threshold frogiveness starting at weight {threshold} is {threshold_boolean} at {threshold_forgiveness}\n")

    return rps

def stemPlot(x,y, title = "Plot",xAxis = "xAxis", yAxis = "yAxis"):
    plt.stem(x, y)
    plt.title(title)
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.show()


directory_path = input("Enter the path to the directory containing csv files: ")
if os.path.isdir(directory_path):
    # calculate the rps and enumerate each file
        rps = calculate_risk(directory_path)
        idx = range(1, len(rps)+1)
        # print out the mean RP for the Directory
        print(f"mean RP: {np.mean(rps):.2f}%")
        # Plot the RP values 
        stemPlot(idx, rps,"Risk Percentage of python files","Python Program","Risk Percentage")
else:
    print("Invalid directory path")
    exit

