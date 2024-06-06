import os
import pandas as pd

# Function to process a single CSV file
def process_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Loop through each column in the DataFrame
    for col in df.columns:
        # Check if the column name ends with "homology type"
        if col.endswith("homology type"):
            # Identify the columns to modify
            col_idx = df.columns.get_loc(col)
            if col_idx < 2:
                raise ValueError(f"Not enough columns before '{col}' to delete values.")
            col1, col2, col3 = df.columns[col_idx - 2], df.columns[col_idx - 1], col
            
            # Apply the condition and modify the DataFrame
            mask = df[col3] != "ortholog_one2one"
            df.loc[mask, [col1, col2, col3]] = None
    
    # Save the modified DataFrame back to a CSV file
    output_path = f"modified_{os.path.basename(file_path)}"
    df.to_csv(output_path, index=False)
    print(f"Processed file saved as {output_path}")

# Function to process all CSV files in a directory
def process_all_csvs(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(""):
            file_path = os.path.join(directory, file_name)
            process_csv(file_path)

# Example usage: Process all CSV files in the 'csv_files' directory
process_all_csvs('z')
