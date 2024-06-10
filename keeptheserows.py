import pandas as pd

# Define the list of columns you want to keep
columns_to_keep = ["ENSEMBL gene ID",
'E1_SPLE3770',
'E1_SPLE3773',
'E1_SPLE3842',
'E1_SPLE3886',
'E4_Spleen1',
'E4_Spleen2',
'E4_Spleen3'
]
  # Modify this list as needed

# Function to filter columns in a TSV file
def filter_columns(input_file, output_file, columns):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(input_file, sep='\t')
    
    # Filter the DataFrame to keep only the specified columns
    filtered_df = df[columns]
    
    # Write the filtered DataFrame to a new TSV file
    filtered_df.to_csv(output_file, sep='\t', index=False, header = True)

# Provide the input and output file paths
input_file_path = 'expressiondata/COW/genes_with_Bips_expression_data_Cow.tsv'
output_file_path = 'Cow_Bip_Exp_Spleen.txt'

# Call the function with the file paths and columns to keep
filter_columns(input_file_path, output_file_path, columns_to_keep)

print(f"Filtered columns saved to {output_file_path}")
import pandas as pd

# Function to filter rows based on identifiers in a text file
def filter_rows_by_identifiers(tsv_file, txt_file, output_file, id_column):
    # Read the identifiers from the text file into a list
    with open(txt_file, 'r') as f:
        identifiers = f.read().splitlines()
    
    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, sep='\t')
    
    # Filter the DataFrame to keep only the rows with identifiers in the list
    filtered_df = df[df[id_column].isin(identifiers)]
    
    # Write the filtered DataFrame to a new TSV file
    filtered_df.to_csv(output_file, sep='\t', index=False)

# Provide the input TSV file, TXT file with identifiers, output file paths, and the name of the column with identifiers
tsv_file_path = 'test.txt'
txt_file_path = 'unique_genes/BIP-btaurus_gene_ensemblunique_values.txt'
output_file_path = 'filtered_output.tsv'
identifier_column = 'ENSEMBL gene ID'  # Change this to the actual column name in your TSV file

# Call the function with the file paths and identifier column name
#filter_rows_by_identifiers(tsv_file_path, txt_file_path, output_file_path, identifier_column)

#print(f"Filtered rows saved to {output_file_path}")
