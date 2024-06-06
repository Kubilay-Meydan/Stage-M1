import os
import pandas as pd
def clean_csv_files(folder_path):
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a CSV
        if filename.endswith(""):
            file_path = os.path.join(folder_path, filename)
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Define a function to check the condition
            def should_delete_row(row):
                non_empty = row.notna()
                # Check if only the first column is populated
                if non_empty[0] and not non_empty[1:-1].any() and not non_empty[-1]:
                    return True
                # Check if only the first and last columns are populated
                if non_empty[0] and not non_empty[1:-1].any() and non_empty[-1]:
                    return True
                return False
            
            # Apply the function to filter rows
            filtered_df = df[~df.apply(should_delete_row, axis=1)]
            
            # Save the cleaned CSV back to the file
            filtered_df.to_csv(file_path, index=False)

# Usage example
folder_path = 'z'  # Replace with the path to your folder
clean_csv_files(folder_path)