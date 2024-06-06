import os
import pandas as pd

def add_bip_number_column(folder_path):
    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path)]

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        
        # Read the CSV file
        df = pd.read_csv(file_path, sep= ",")
        
        # Insert the BIP number column at the first position
        df.insert(0, 'BIP number', range(1, len(df) + 1))
        
        # Save the modified CSV back to the folder
        df.to_csv(file_path, index=False)
        print(f'Processed {file}')

# Example usage
folder_path = "sheep stuff"  # Replace with your folder path
add_bip_number_column(folder_path)
