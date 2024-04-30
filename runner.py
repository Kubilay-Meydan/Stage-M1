from biomart import BiomartServer
import pandas as pd
import Biomart_Getter
import os
import finder 



# Initialize the Biomart server
server = BiomartServer("http://www.ensembl.org/biomart")

# List to store datasets
genes_datasets = [i for i in server.datasets if i.endswith("gene_ensembl")]

# Define the results directory
results_dir = "results"

# Process each dataset
for dataset in genes_datasets:
    results_path = os.path.join(results_dir, f"{dataset}")

    # Skip processing if the file already exists
    if os.path.exists(results_path):

        print(f"File {results_path} already exists. Skipping...")
    else:
        print("getting " + dataset)

        # Retrieve and save CSV
        csv_data = Biomart_Getter.getCSV(dataset=dataset)
        Biomart_Getter.write_csv(csv_data, results_path)

        # Filter and update the CSV in place
        Biomart_Getter.filter_chromosome(results_path, results_path)


# Iterate over all CSV files in the results directory
for filename in os.listdir(results_dir):
    if filename.endswith(""):


        # Check if the file is not just a header by reading it into a DataFrame


            # Check if the DataFrame is empty (i.e., no data beyond headers)

            # Assuming you have a corresponding BIP filename convention or logic
            bip_filename = "BIP-" + filename  # Update this line as needed based on actual BIP filename logic

                # Run the finder function
            finder.find_potential_close_BIPs("results/"+filename, os.path.join(results_dir,"BIPS/" + bip_filename))

