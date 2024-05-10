import os
import pandas as pd

# Define the directory containing your CSV files
directory = "results/BIPS"

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV
    if filename.endswith(''):
        file_path = os.path.join(directory, filename)
        
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path, sep= '\t')
            
            # Check if the 'Chromosome/scaffold name' column exists
            if 'Chromosome/scaffold name' in df.columns:
                # Check if all values in the column are 'MT'
                if all(df['Chromosome/scaffold name'] == 'MT'):
                    print(filename)
                    os.remove(file_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# If you need to handle cases with different column names that mean the same thing,
# you could add more checks or preprocess the column names.
