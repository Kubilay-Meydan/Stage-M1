import pandas as pd

def find_potential_close_BIPs(csv_input, csv_output):
    try:
        # Load the data and sort it
        data = pd.read_csv(csv_input, sep='\t')
        data.sort_values(by=['Chromosome/scaffold name', 'Gene start (bp)'], inplace=True)

        # Create an empty list to store results
        results = []

        # Iterate through sorted data
        previous_row = None
        for index, current_row in data.iterrows():
            if previous_row is not None and previous_row['Chromosome/scaffold name'] == current_row['Chromosome/scaffold name']:
                # Calculate distances
                distance1 = abs(previous_row['Gene end (bp)'] - current_row['Gene start (bp)'])
                distance2 = abs(current_row['Gene end (bp)'] - previous_row['Gene start (bp)'])
                min_distance = min(distance1, distance2)

                # Check distance condition
                if min_distance < 1000:
                    # Check strand condition
                    if previous_row['Strand'] * current_row['Strand'] == -1:
                        # Combine rows into one row with all columns and add distance at the end
                        combined_row = pd.concat([previous_row, current_row]).to_frame().T
                        combined_row.reset_index(drop=True, inplace=True)
                        combined_row['distance'] = min_distance

                        # Append the combined row to the results list
                        results.append(combined_row)

            previous_row = current_row

        # Concatenate all results into a single DataFrame
        if results:
            results_df = pd.concat(results, ignore_index=True)
        else:
            results_df = pd.DataFrame()

        # Write the results to a new CSV file
        results_df.to_csv(csv_output, index=False, sep = '\t')
        
    except Exception as e:
        print(f"An error occurred: {e}")



#find_potential_close_BIPs("clean.csv", "bip.csv")