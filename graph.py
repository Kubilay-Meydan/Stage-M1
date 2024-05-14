import os
import pandas as pd
import matplotlib.pyplot as plt

pie_chart_colors = [
    "#BF7BA7ff",  # sky-magenta
    "#F5C9C2ff",  # tea-rose-red
    "#FDF1E8ff",  # linen
    "#FEC7E3ff",  # fairy-tale
    "#C699A6ff",  # puce
    "#323644ff",  # gunmetal
    "#ABBCE1ff",  # powder-blue
    "#E9E3E8ff",  # magnolia
    "#F0D5D4ff",  # misty-rose
    "#BF87CCff"  # african-violet
]


def histogramme_ratio():
    # Define paths
    complete_files_folder = "results"
    bips_files_folder = "results\\BIPS"

    # Get list of complete files and bips files
    complete_files = [f for f in os.listdir(complete_files_folder)]
    bips_files = [f for f in os.listdir(bips_files_folder) if f.startswith('BIP-')]

    ratios = []

    for bip_file in bips_files:
        # Find corresponding complete file
        complete_file = bip_file[4:]

        if complete_file in complete_files:
            # Read the files
            bip_df = pd.read_csv(os.path.join(bips_files_folder, bip_file), sep='\t')
            complete_df = pd.read_csv(os.path.join(complete_files_folder, complete_file), sep='\t')

            # Calculate the ratio of number of rows
            ratio = (len(bip_df) * 2) / len(complete_df)
            print(ratio)
            ratios.append(ratio)

    # Plot histogram of the ratios
    plt.hist(ratios, bins=10, edgecolor='black')
    plt.xlabel("Ratio du nombre de bips par rapport au nombre de genes de l'espece")
    plt.ylabel('Fréquence')
    plt.title('Histogramme du nombre de BIPS par rapport au nombre de genes')
    plt.savefig("histogramme_ratio.png")
    plt.show()

def create_gene_type_pie_charts():
    bips_files_folder = "results\\BIPS"
    output_folder = "pie_charts"
    mapping_csv_path = "summary+phylo.csv"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the mapping CSV file
    mapping_df = pd.read_csv(mapping_csv_path)
    mapping_dict = mapping_df.set_index('id')['Species Name'].to_dict()

    # Get list of BIPS files
    bips_files = [f for f in os.listdir(bips_files_folder) if f.startswith('BIP-')]
    for bip_file in bips_files:
        bip_df = pd.read_csv(os.path.join(bips_files_folder, bip_file), sep='\t')

        # Get the ID from the BIP file name
        bip_id = bip_file.split('_')[0][4:]  # Extract the 'x' from 'BIP-x_...'

        # Get the species name from the mapping dictionary
        species_name = mapping_dict.get(bip_id, bip_file)  # Default to bip_file if not found

        # Get gene type columns
        gene_combinations = bip_df[['Gene type', 'Gene type']].apply(tuple, axis=1).value_counts()

        labels = [f'{combo[0]} & {combo[1]}' for combo in gene_combinations.index]
        sizes = gene_combinations.values
        total = sum(sizes)
        percentages = [f'{size/total*100:.1f}%' for size in sizes]
        legend_labels = [f'{label}: {percentage}' for label, percentage in zip(labels, percentages)]

        plt.figure(figsize=(15, 15))
        wedges, _ = plt.pie(sizes, startangle=140, colors=pie_chart_colors[:len(sizes)])

        plt.title(f'Gene Type Combinations for {species_name}')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Add a legend anchored to the right corner
        plt.legend(wedges, legend_labels, title="Gene Type Combinations", loc="upper left", bbox_to_anchor=(0.6, 0.6), fontsize='small')

        # Save the pie chart as a PNG file
        output_path = os.path.join(output_folder, f'{species_name}_gene_type_pie_chart.png')
        plt.savefig(output_path)
        plt.close()
        
# Uncomment the next line to run the histogram function and save it as a PNG file
#histogramme_ratio()

# Call the function to create pie charts and save them as PNG files
create_gene_type_pie_charts()
