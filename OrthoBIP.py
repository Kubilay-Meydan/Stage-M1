import pandas as pd

# Function to load CSV files
def load_csv(file_path):
    return pd.read_csv(file_path)

# Function to map base species genes to their compared species orthologs
def create_ortholog_map(ortholog_df, base_species_prefix, compared_species_prefix):
    ortholog_map = {}
    for _, row in ortholog_df.iterrows():
        base_gene_id = row['Gene stable ID']
        compared_gene_id = row[f'{compared_species_prefix} gene stable ID']
        if not pd.isna(base_gene_id) and not pd.isna(compared_gene_id):
            ortholog_map[base_gene_id] = compared_gene_id
    return ortholog_map

# Function to find matching ortholog pairs
def find_matching_ortholog_pairs(base_bip, compared_bip, ortholog_map):
    matching_pairs = []

    for _, base_row in base_bip.iterrows():
        base_gene_1 = base_row['Gene stable ID']
        base_gene_2 = base_row['Gene stable ID.1']

        if base_gene_1 in ortholog_map and base_gene_2 in ortholog_map:
            compared_gene_1 = ortholog_map[base_gene_1]
            compared_gene_2 = ortholog_map[base_gene_2]

            # Check if the compared species genes are in the same BIP line
            matching_compared_row = compared_bip[
                (compared_bip['Gene stable ID'] == compared_gene_1) &
                (compared_bip['Gene stable ID.1'] == compared_gene_2)
            ]

            if not matching_compared_row.empty:
                base_bip_number = base_row['BIP number']
                compared_bip_number = matching_compared_row.iloc[0]['BIP number']
                matching_pairs.append([base_bip_number, compared_bip_number])

    return matching_pairs

# Main function to process the files
def process_files(ortholog_file, base_bip_file, compared_bip_file, base_species_prefix, compared_species_prefix, output_file):
    ortholog_df = load_csv(ortholog_file)
    base_bip = load_csv(base_bip_file)
    compared_bip = load_csv(compared_bip_file)

    ortholog_map = create_ortholog_map(ortholog_df, base_species_prefix, compared_species_prefix)

    matching_pairs = find_matching_ortholog_pairs(base_bip, compared_bip, ortholog_map)

    # Save the matching pairs to a CSV file
    matching_df = pd.DataFrame(matching_pairs, columns=[f'{base_species_prefix} BIP number', f'{compared_species_prefix} BIP number'])
    matching_df.to_csv(output_file, index=False)

# Example usage
ortholog_file = 'orthologs2/MICE_2.txt'
base_bip_file = 'results/BIPS/BIP-mmusculus_gene_ensembl'
compared_bip_file = 'results/BIPS/BIP-rnorvegicus_gene_ensembl'
base_species_prefix = 'Mouse'  # Change to the base species prefix
compared_species_prefix = 'Rat'  # Change to the compared species prefix
output_file = 'Mouse_Rat_pairs.csv'

process_files(ortholog_file, base_bip_file, compared_bip_file, base_species_prefix, compared_species_prefix, output_file)
