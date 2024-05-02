import os

def check_empty_csv_files(directory):
    # List to hold the names of empty CSV files
    empty_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a CSV file
            if file.endswith(''):
                file_path = os.path.join(root, file)
                
                # Open and check if the file is empty
                try:
                    with open(file_path, 'r') as f:
                        data = f.readline()
                        # Check if the data line is empty
                        if not data.strip():
                            #file = file[4:]
                            empty_files.append(file)
                except IOError as e:
                    print(f"Error opening file {file_path}: {e}")

    return empty_files

def remove_files_from_directory(file_list, directory):
    # Iterate through each file in the file list
    for file_name in file_list:
        # Construct the full path to the file
        file_path = os.path.join(directory, file_name)
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Try to remove the file
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            except Exception as e:
                print(f"Failed to remove {file_path}. Reason: {e}")
        else:
            print(f"File does not exist: {file_path}")

directory = 'results/BIPS'
empty_csv_files = check_empty_csv_files(directory)
print("Empty CSV files:", empty_csv_files)
remove_files_from_directory(empty_csv_files,directory)
