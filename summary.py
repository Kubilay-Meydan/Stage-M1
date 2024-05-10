import os
import csv
from biomart import BiomartServer

# Define the directory containing your files
directory = "results/BIPS"

# Define the output CSV file path
output_csv_path = os.path.join("summary.csv")

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

def count_rows(filepath):
    with open(filepath, 'r') as f:
        # Create a CSV reader to handle tab-delimited files
        reader = csv.reader(f, delimiter='\t')
        return sum(1 for row in reader)

# Open a CSV file to write the output
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Species Name', 'Number of BIPS', 'Dataset Number', 'id'])

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith('BIP-') and filename.endswith('_gene_ensembl'):
            # Extract the dataset identifier from the filename
            # Remove 'BIP-' from the start and '_gene_ensembl' from the end
            dataset_id = filename[4:].split('_gene_ensembl')[0]

            # Use the dataset identifier to query the BioMart server
            try:
                # Access the dataset from the server
                ds = server.datasets[f"{dataset_id}_gene_ensembl"]
                
                # Extract the species name and dataset number
                species_name = str(ds).split(' (')[0]
                dataset_number = str(ds).split(' (')[1][:-1]

                # Determine the number of columns (BIPS) in the file
                file_path = os.path.join(directory, filename)
                bips = count_rows(file_path) -1

                # Print out the information (optional, for debugging)
                print(f"Processing {filename}:")
                print(f"Species Name: {species_name}, Dataset Number: {dataset_number}, BIPS: {bips}")

                # Write the row to the CSV file
                writer.writerow([species_name, bips, dataset_number, dataset_id])

            except Exception as e:
                print(f"Error processing {filename}: {e}\n")
