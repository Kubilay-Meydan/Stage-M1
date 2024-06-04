import pandas as pd
import os

def transform_header(header):
    species_name = header.split('_BIP_number')[0].replace('_', ' ').title().replace(' ', '_')
    return [
        f"{species_name}_BIP number",
        f"{species_name}_Gene stable ID",
        f"{species_name}_Chromosome/scaffold name",
        f"{species_name}_Gene start (bp)",
        f"{species_name}_Gene end (bp)",
        f"{species_name}_Strand",
        f"{species_name}_Gene description",
        f"{species_name}_Gene name",
        f"{species_name}_Gene type",
        f"{species_name}_Gene stable ID.1",
        f"{species_name}_Chromosome/scaffold name.1",
        f"{species_name}_Gene start (bp).1",
        f"{species_name}_Gene end (bp).1",
        f"{species_name}_Strand.1",
        f"{species_name}_Gene description.1",
        f"{species_name}_Gene name.1",
        f"{species_name}_Gene type.1",
        f"{species_name}_distance"
    ]

def transform_csv(input_csv_path, output_txt_path, summary_csv_path, bip_folder):
    # Load the CSV files
    df = pd.read_csv(input_csv_path)
    summary_df = pd.read_csv(summary_csv_path)

    print("Input CSV loaded")
    print("Summary CSV loaded")

    # Get the new headers
    new_headers = []
    for col in df.columns:
        new_headers.extend(transform_header(col))

    # Create a new DataFrame with the new headers
    new_df = pd.DataFrame(columns=new_headers)

    # Fill the new DataFrame with data from the bip files
    for i, row in df.iterrows():
        new_row = []
        for col in df.columns:
            species_name = col.split('_BIP_number')[0].replace('_', ' ').title()
            species_with_genes = f"{species_name} Genes"
            species_row = summary_df[summary_df['Species Name'].str.replace('_', ' ').str.title() == species_with_genes]

            if not species_row.empty:
                species_id = species_row['id'].values[0]
                bip_number = row[col]
                bip_file = os.path.join(bip_folder, f"BIP-{species_id}_gene_ensembl")

                #print(f"Checking file: {bip_file}")
                if os.path.exists(bip_file):
                    bip_df = pd.read_csv(bip_file)
                    bip_row = bip_df[bip_df['BIP number'] == bip_number]

                    if not bip_row.empty:
                        #print(f"Found BIP number {bip_number} in file {bip_file}")
                        bip_row_data = bip_row.iloc[0].tolist()
                        new_row.extend(bip_row_data)
                    else:
                        #print(f"BIP number {bip_number} not found in file {bip_file}")
                        new_row.extend([None] * 18)  # Assuming there are 18 columns in the bip file
                else:
                    #print(f"File does not exist: {bip_file}")
                    new_row.extend([None] * 18)
            else:
                #print(f"Species {species_with_genes} not found in summary file")
                new_row.extend([None] * 18)

        new_df.loc[i] = new_row

    # Save the new DataFrame as a TXT file with tab as separator
    new_df.to_csv(output_txt_path, sep='\t', index=False)
    print(f"Output TXT saved to {output_txt_path}")

# Usage example:
input_csv_path = 'BIP orthologs/Mice/Combined_Mouse_BIP_numbers.csv'  # Path of your input CSV file
output_txt_path = 'Mice-BIP_Full.txt'  # Path where you want to save the output TXT file
summary_csv_path = 'summary+phylo.csv'  # Path to your summary CSV file
bip_folder = 'results/BIPS'  # Folder containing the bip files

# Transform the CSV
transform_csv(input_csv_path, output_txt_path, summary_csv_path, bip_folder)
