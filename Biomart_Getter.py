import csv
import pandas as pd
from biomart import BiomartServer

def get_human_mouse_orthologs(serv="http://www.ensembl.org/biomart", dataset='hsapiens_gene_ensembl', verbose=False):
    server = BiomartServer(serv)
    server.verbose = verbose
    human_genes = server.datasets[dataset]

    attributes = [
        'ensembl_gene_id',
        'external_gene_name'
    ]

    response = human_genes.search({
        'attributes': attributes
    }, header=1)
    
    human_gene_list = []
    for line in response.iter_lines():
        decoded_line = line.decode('utf-8')
        if not decoded_line.startswith('#'):
            ensembl_gene_id, gene_name = decoded_line.split("\t")
            human_gene_list.append((ensembl_gene_id, gene_name))
    
    return human_gene_list

def get_mouse_orthologs(human_gene_list, serv="http://www.ensembl.org/biomart", dataset='mmusculus_gene_ensembl', verbose=False):
    server = BiomartServer(serv)
    server.verbose = verbose
    mouse_genes = server.datasets[dataset]
    
    orthologs = []
    
    for human_gene_id, human_gene_name in human_gene_list:
        response = mouse_genes.search({
            'filters': {'with_homolog': '1', 'with_human_ortholog': human_gene_id},
            'attributes': ['ensembl_gene_id', 'external_gene_name']
        }, header=1)
        
        for line in response.iter_lines():
            decoded_line = line.decode('utf-8')
            if not decoded_line.startswith('#'):
                mouse_gene_id, mouse_gene_name = decoded_line.split("\t")
                orthologs.append((human_gene_id, human_gene_name, mouse_gene_id, mouse_gene_name))
    
    return orthologs

def write_orthologs_to_csv(orthologs, destination):
    with open(destination, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(['Human Ensembl Gene ID', 'Human Gene Name', 'Mouse Ensembl Gene ID', 'Mouse Gene Name'])
        for ortholog in orthologs:
            writer.writerow(ortholog)

# Example usage:
human_gene_list = get_human_mouse_orthologs(verbose=True)
mouse_orthologs = get_mouse_orthologs(human_gene_list, verbose=True)
write_orthologs_to_csv(mouse_orthologs, 'human_mouse_orthologs.csv')

def filter_chromosome(csv_input, csv_output):
    data = pd.read_csv(csv_input, delimiter='\t')

    # Define the valid chromosome names
    valid_chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y', 'W', 'Z', 'MT']

    filtered_data = data[data['Chromosome/scaffold name'].isin(valid_chromosomes)]

    filtered_data.to_csv(csv_output, index=False, sep='\t')

# Example usage of filter_chromosome:
# filter_chromosome("human_mouse_orthologs.csv", 'filtered_orthologs.csv')
