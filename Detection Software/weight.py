import csv
import glob
import os

def calculate_risk(directory_path):
    # Constants
    constant_for_saf = 90  # Modify as needed
    threshold = 30
    threshold_forgiveness = 0.5

    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))
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
                        print(row) #TODO Delete when done, just debugging tool.
                elif 'function' in row['Type'].lower():
                    mf += int(row['Weight'])
                    tf += 1
                    tl += 1
                    if(int(row['Weight']) >= threshold):
                        threshold_boolean = False 
                        print(row) #TODO Delete when done, just debugging tool.

        # Calculate SAF (Scale Adjustment Factor)
        if (threshold_boolean == True):
            ml = ml * threshold_forgiveness
            mf = mf * threshold_forgiveness
        saf = 1 + (constant_for_saf / (tl if tl > tf else tf))

        # Calculate Risk Percentage (RP)
        rp = ((ml + mf) / (tf if tf > 0 else 1)) * saf

        print(f"Risk analysis for {os.path.basename(csv_file)}:")
        print(f"  ML (Malicious Libraries): {ml}")
        print(f"  MF (Malicious Functions): {mf}")
        print(f"  TL (Total Lines): {tl}")
        print(f"  TF (Total Functions): {tf}")
        print(f"  SAF (Scale Adjustment Factor): {saf:.2f}")
        print(f"  RP (Risk Percentage): {rp:.2f}%")
        print(f"  Threshold frogiveness starting at weight {threshold} is {threshold_boolean} at {threshold_forgiveness}\n")

# Example usage
os.chdir(os.path.dirname(__file__))
os.chdir('../')
directory_path = os.path.join(os.getcwd(), 'RansomWare/python files')
calculate_risk(directory_path)
