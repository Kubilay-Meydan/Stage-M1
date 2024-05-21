import os
import shutil

def get_files_in_directory(directory):
    return set(os.listdir(directory))

def delete_extra_files(source_dir, target_dir):
    source_files = get_files_in_directory(source_dir)
    target_files = get_files_in_directory(target_dir)
    
    # Check if all files in source_dir are in target_dir
    if source_files.issubset(target_files):
        # Delete extra files in target_dir
        extra_files = target_files - source_files
        for file in extra_files:
            file_path = os.path.join(target_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Deleted directory: {file_path}")
        print("All extra files deleted.")
    else:
        print("Not all files from the source directory are present in the target directory. No files deleted.")

# Example usage:
source_directory = 'results/BIPS'  # Replace with the path to your source directory (dir A)
target_directory = 'results2/BIPS'  # Replace with the path to your target directory (dir B)

delete_extra_files(source_directory, target_directory)
