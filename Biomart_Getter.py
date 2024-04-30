from biomart import BiomartServer
import csv

server = BiomartServer("http://www.ensembl.org/biomart")
genes = server.datasets['hsapiens_gene_ensembl']

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

def write_csv(response):
    with open('ensembl_genes.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for line in response.iter_lines():
            decoded_line = line.decode('utf-8')
            writer.writerow(decoded_line.split("\t"))



write_csv(getCSV())