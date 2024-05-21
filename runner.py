from biomart import BiomartServer
import pandas as pd
import Biomart_Getter
import os
import finder 



server = BiomartServer("http://www.ensembl.org/biomart")

genes_datasets = [i for i in server.datasets if i.endswith("gene_ensembl")]


results_dir = "results2"


for dataset in genes_datasets:
    results_path = os.path.join(results_dir, f"{dataset}")


    if os.path.exists(results_path):

        print(f"File {results_path} already exists. Skipping...")
    else:
        print("getting " + dataset)

        csv_data = Biomart_Getter.getCSV(dataset=dataset)
        Biomart_Getter.write_csv(csv_data, results_path)

        Biomart_Getter.filter_chromosome(results_path, results_path)


for filename in os.listdir(results_dir):
    if filename.endswith(""):
        if os.path.exists("results2/BIPS/" + "BIP-" + filename):

            print(f"File {results_path} BIP already exists. Skipping...")
        else:

            bip_filename = "BIP-" + filename
            finder.find_potential_close_BIPs("results/"+filename, os.path.join(results_dir,"BIPS/" + bip_filename))
