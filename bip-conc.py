import os
import pandas as pd


bip_folder = 'results/BIPS'
mapping_csv = 'summary+phylo.csv'

mapping_df = pd.read_csv(mapping_csv)

concatenated_df = pd.DataFrame()

for file_name in os.listdir(bip_folder):
    if file_name.endswith(''):
        species_id = file_name.split('-')[1].split('_')[0]

        file_path = os.path.join(bip_folder, file_name)
        temp_df = pd.read_csv(file_path)
        
        species_name = mapping_df.loc[mapping_df['id'] == species_id, 'Species Name'].values[0]

        temp_df.insert(0, 'Species Name', species_name)

        concatenated_df = pd.concat([concatenated_df, temp_df], ignore_index=True)

output_csv = 'conc.csv'
concatenated_df.to_csv(output_csv, index=False)

print(f"Concatenated CSV file saved to {output_csv}")