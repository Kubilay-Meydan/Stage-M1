import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_csv(file_name):
    print(f"Loading CSV file: {file_name}")
    return pd.read_csv(file_name, delimiter=',')

def fetch_orthologs(gene_id, target_species):
    url = f"https://rest.ensembl.org/homology/id/{gene_id}?content-type=application/json;type=orthologues;target_species={target_species}"
    response = requests.get(url, headers={"Content-Type": "application/json"})

    if not response.ok:
        return []

    data = response.json()
    orthologs = [homology['target']['id'] for homology in data['data'][0]['homologies']]
    return orthologs

def get_orthologs(gene_id, target_species, cache):
    if gene_id in cache:
        return cache[gene_id]
    orthologs = fetch_orthologs(gene_id, target_species)
    cache[gene_id] = orthologs
    return orthologs

def check_orthologs(species_list):
    cache = {}
    common_orthologs = []

    def process_pair(species1, row):
        gene_id1 = row['Gene stable ID']
        gene_id2 = row['Gene stable ID.1']

        orthologs1 = get_orthologs(gene_id1, species1['name'], cache)
        orthologs2 = get_orthologs(gene_id2, species1['name'], cache)

        results = []

        for species2 in species_list:
            if species1 == species2:
                continue

            species2_df = load_csv(species2['file'])

            for i, row2 in species2_df.iterrows():
                if row2['Gene stable ID'] in orthologs1 and row2['Gene stable ID.1'] in orthologs2:
                    results.append({
                        'Species 1': species1['name'],
                        'Gene 1': gene_id1,
                        'Gene 2': gene_id2,
                        'Species 2': species2['name'],
                        'Ortholog 1': row2['Gene stable ID'],
                        'Ortholog 2': row2['Gene stable ID.1']
                    })
        return results

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for species1 in species_list:
            species1_df = load_csv(species1['file'])
            for index, row in species1_df.iterrows():
                futures.append(executor.submit(process_pair, species1, row))

        for future in as_completed(futures):
            common_orthologs.extend(future.result())

    return common_orthologs

def main():
    species_list = [
        {'name': 'horse', 'file': 'results/BIPS/BIP-ecaballus_gene_ensembl'}, 
        {'name': 'donkey', 'file': 'results/BIPS/BIP-easinus_gene_ensembl'}, 

    ]

    print("Starting to check for orthologous pairs")
    common_orthologs = check_orthologs(species_list)

    if common_orthologs:
        print("Common orthologous pairs found:")
        for ortholog in common_orthologs:
            print(ortholog)
    else:
        print("No common orthologous pairs found.")

if __name__ == "__main__":
    main()
