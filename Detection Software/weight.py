import csv
import glob
import os

def calculate_risk(directory_path):
    # Constants
    constant_for_saf = 10  # Modify as needed

    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))
    for csv_file in csv_files:
        ml, mf, tl, tf = 0, 0, 0, 0

        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Type'] in ['Import', 'Import ... from ...']:
                    ml += int(row['Weight'])
                    tl += 1
                elif 'function' in row['Type'].lower():
                    mf += int(row['Weight'])
                    tf += 1
                    tl += 1

        # Calculate SAF (Scale Adjustment Factor)
        saf = 1 + (constant_for_saf / (tl if tl > tf else tf))
        
        # Calculate Risk Percentage (RP)
        rp = ((ml + mf) / (tf if tf > 0 else 1)) * saf

        print(f"Risk analysis for {os.path.basename(csv_file)}:")
        print(f"  ML (Malicious Libraries): {ml}")
        print(f"  MF (Malicious Functions): {mf}")
        print(f"  TL (Total Lines): {tl}")
        print(f"  TF (Total Functions): {tf}")
        print(f"  SAF (Scale Adjustment Factor): {saf:.2f}")
        print(f"  RP (Risk Percentage): {rp:.2f}%\n")

# Example usage
directory_path = 'C:/Users/Pause/Documents/GitHub/RandomWare-CSProj-G15/RansomWare/python files'  # Update with the path to your CSV files
calculate_risk(directory_path)
