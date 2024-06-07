import pandas as pd

def find_potential_close_BIPs(csv_input, csv_output):
    try:
        # Load data
        data = pd.read_csv(csv_input, sep='\t')
        data.sort_values(by=['Chromosome/scaffold name', 'Gene start (bp)'], inplace=True)

        results = []

        previous_row = None
        for index, current_row in data.iterrows():
            if previous_row is not None and previous_row['Chromosome/scaffold name'] == current_row['Chromosome/scaffold name']:
                distance1 = abs(previous_row['Gene end (bp)'] - current_row['Gene start (bp)'])
                distance2 = abs(current_row['Gene end (bp)'] - previous_row['Gene start (bp)'])
                min_distance = min(distance1, distance2)

                if min_distance < 1000:
                    if previous_row['Strand'] * current_row['Strand'] == -1:
                        combined_row = pd.concat([previous_row, current_row]).to_frame().T
                        combined_row.reset_index(drop=True, inplace=True)
                        combined_row['distance'] = min_distance
                        results.append(combined_row)

            previous_row = current_row

        if results:
            results_df = pd.concat(results, ignore_index=True)
            # Renaming the second set of column names
            results_df.columns = [f"{col}.1" if i >= len(data.columns) else col for i, col in enumerate(results_df.columns)]
        else:
            results_df = pd.DataFrame()

        results_df.to_csv(csv_output, index=False, sep=',')

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
find_potential_close_BIPs("results/bbison_gene_ensembl", "BIP-bbison_gene_ensembl")
