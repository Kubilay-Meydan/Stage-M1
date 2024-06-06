import os
import pandas as pd

# Specify the folder containing the CSV files and the base species
folder_path = 'BIP orthologs/Cattle'  # Replace with the actual path to your folder
base_species = 'Cow'   # Replace with the actual base species name

# List to hold all dataframes
dataframes = []
species_columns = []

# Loop through all files in the specified directory
for file in os.listdir(folder_path):
    if file.endswith("matching_pairs.csv"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, dtype=str)  # Read CSV as strings
        # Extract species names from the filename
        parts = file.replace("matching_pairs.csv", "").split('_')
        base_species_in_file = parts[0]
        reference_species = parts[1]
        
        if base_species_in_file != base_species:
            continue  # Skip files that don't match the specified base species
        
        if len(dataframes) == 0:
            # Rename columns to include the species for clarity
            df.columns = [f'{base_species}_BIP_number', f'{reference_species}_BIP_number']
        else:
            # Rename columns to include the species for clarity, ensure the base species column is consistent
            df.columns = [f'{base_species}_BIP_number', f'{reference_species}_BIP_number']
            
        dataframes.append(df)
        species_columns.append(f'{reference_species}_BIP_number_{len(dataframes)}')

# Merge all dataframes on the base species BIP number column
combined_df = dataframes[0]
for df in dataframes[1:]:
    combined_df = pd.merge(combined_df, df, on=f'{base_species}_BIP_number', how='outer')

# Ensure the combined dataframe is filled with empty strings for NaNs to avoid float conversion
combined_df = combined_df.fillna('')

# Save the combined dataframe to a new CSV file
combined_df.to_csv(os.path.join(folder_path, f'Combined_{base_species}_BIP_numbers.csv'), index=False)

print("Combined CSV file created successfully.")
