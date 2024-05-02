import os

def check_empty_csv_files(directory):
    empty_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(''):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r') as f:
                        data = f.readline()
                        if not data.strip():
                            empty_files.append(file)
                except IOError as e:
                    print(f"Error opening file {file_path}: {e}")

    return empty_files

def remove_files_from_directory(file_list, directory):
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        
        if os.path.exists(file_path):
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
