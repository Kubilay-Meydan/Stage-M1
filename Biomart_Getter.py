from biomart import BiomartServer
import csv
import pandas as pd


def getCSV(serv = "http://www.ensembl.org/biomart", dataset = 'hsapiens_gene_ensembl', verbose = False):
    server = BiomartServer(serv)
    genes = server.datasets[dataset]
    server.verbose = verbose 
    #Genes111datasets = []
    #for i in server.datasets:
    #    if i.endswith("gene_ensembl"):
    #        Genes111datasets.append(i)
    # print(len(Genes111datasets)) 229 
    #print(Genes111datasets)

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

#write_csv(getCSV(verbose = True))


def filter_chromosome(csv_input, csv_output):

    # Read the data from the CSV file
    data = pd.read_csv(csv_input, delimiter='\t')
    
    # Filter the data to keep rows where 'Chromosome/scaffold name' is a digit or 'MT'
    filtered_data = data[data['Chromosome/scaffold name'].apply(lambda x: str(x).isdigit() or str(x) == 'MT')]

    # Write the filtered data to a new CSV file
    filtered_data.to_csv(csv_output, index=False, sep='\t')


#filter_chromosome('ensembl_genes.csv', 'clean.csv')