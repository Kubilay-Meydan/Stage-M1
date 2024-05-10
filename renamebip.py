import os
from biomart import BiomartServer

# Define the directory containing your files
directory = "results/BIPS"

# Initialize the BioMart server
server = BiomartServer("http://www.ensembl.org/biomart")

# A helper function to sanitize filenames
def sanitize_filename(name):
    return (name.replace('<', '')
                .replace('>', '')
                .replace(':', '-')
                .replace('"', '')
                .replace('/', '-')
                .replace('\\', '-')
                .replace('|', '-')
                .replace('?', '')
                .replace('*', ''))

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('_gene_ensembl'):
        # Extract the dataset identifier from the filename
        dataset_id = filename.split('_gene_ensembl')[0]

        # Use the dataset identifier to query the BioMart server
        try:
            # Access the dataset from the server
            ds = server.datasets[f"{dataset_id}_gene_ensembl"]
            
            # Extract the species name and dataset number
            species_name = str(ds).split(' (')[0]
            dataset_number = str(ds).split(' (')[1][:-1]

            # Print out the information (optional)
            print(f"Processing {filename}:")
            print(f"Species Name: {species_name}, Dataset Number: {dataset_number}")

            # Sanitize the species name to ensure it's a valid filename
            sanitized_species_name = sanitize_filename(species_name)

            # Define the new filename
            new_filename = f"{sanitized_species_name}"

            # Full path for old and new filenames
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}\n")

        except Exception as e:
            print(f"Error processing {filename}: {e}\n")