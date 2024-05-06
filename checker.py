import os
import re

def extract_name_from_filename(filename):
    match = re.search(r'BIP-(\w+)_gene_ensembl', filename)
    if match:
        return match.group(1)
    return None

def check_names_in_newick(directory, newick_path):
    # Read the Newick file
    with open(newick_path, 'r') as file:
        newick_content = file.read()

    missing_files = []

    # Iterate through files in the specified directory
    for filename in os.listdir(directory):
        if 'BIP-' in filename and filename.endswith('_gene_ensembl'):
            name = extract_name_from_filename(filename)
            if name and name not in newick_content:
                missing_files.append(filename)

    return missing_files

# Example usage
directory_path = 'results/BIPS'
newick_file_path = 'taxonomy.nw'
missing = check_names_in_newick(directory_path, newick_file_path)
missinglist = []
if missing:
    print("Files with names not found in the Newick file:")
    for file in missing:
        missinglist.append(file)
        print(file)

else:
    print("All file names are present in the Newick file.")
print(len(missinglist))