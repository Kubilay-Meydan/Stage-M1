from biomart import BiomartServer
import csv
import pandas as pd


def getCSV(serv="http://www.ensembl.org/biomart", dataset='hsapiens_gene_ensembl', verbose=False):
    server = BiomartServer(serv)
    genes = server.datasets[dataset]
    server.verbose = verbose 
    Genes111datasets = []
    for i in server.datasets:
        if i.endswith("gene_ensembl"):
            Genes111datasets.append(i)
    print(len(Genes111datasets))  # 229 
    print(server.datasets["hsapiens_gene_ensembl"])

    attributes = [
        'ensembl_gene_id',
        'chromosome_name',
        'start_position',
        'end_position',
        'strand',
        'description',
        'external_gene_name',
        'gene_biotype'
    ]

    response = genes.search({
        'attributes': attributes
    }, header=1)  # `header=1` to include the column headers
    return response

def write_csv(response, destination):
    with open(destination, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for line in response.iter_lines():
            decoded_line = line.decode('utf-8')
            writer.writerow(decoded_line.split("\t"))

getCSV(dataset="abrachyrhynchus_gene_ensembl", verbose=True)


def filter_chromosome(csv_input, csv_output):
    data = pd.read_csv(csv_input, delimiter='\t')

    # Define the valid chromosome names
    valid_chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y', 'W', 'Z', 'MT']

    filtered_data = data[data['Chromosome/scaffold name'].isin(valid_chromosomes)]

    filtered_data.to_csv(csv_output, index=False, sep='\t')

# Example usage:
# filter_chromosome("abrachyrhynchus_gene_ensembl.csv", 'clean.csv')
