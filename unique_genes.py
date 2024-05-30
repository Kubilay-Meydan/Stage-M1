import pandas as pd

# Read the CSV file
input_file = "results/BIPS/BIP-ggallus_gene_ensembl"
df = pd.read_csv(input_file)

# Get unique values from both columns
unique_gene_stable_id = df['Gene stable ID'].unique()
unique_gene_stable_id_1 = df['Gene stable ID.1'].unique()

# Combine the unique values into a single set to avoid duplicates
unique_values = set(unique_gene_stable_id).union(set(unique_gene_stable_id_1))

# Write the unique values to a TXT file
output_file = input_file + 'unique_values.txt'
with open(output_file, 'w') as file:
    for value in unique_values:
        file.write(f"{value}\n")

print(f"Unique values have been written to {output_file}")
