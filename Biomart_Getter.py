from biomart import BiomartServer
import csv
server = BiomartServer("http://www.ensembl.org/biomart")
server.verbose = True

genes = server.datasets['hsapiens_gene_ensembl']
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


with open('ensembl_genes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for line in response.iter_lines():
        decoded_line = line.decode('utf-8')
        writer.writerow(decoded_line.split("\t"))
