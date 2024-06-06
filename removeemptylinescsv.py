import csv

def remove_empty_lines(input_csv, output_csv):
    with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            # Check if row is not empty
            if any(field.strip() for field in row):
                writer.writerow(row)

# Example usage
remove_empty_lines('z\modified_mous_hamsterorthologs', 'output.csv')
