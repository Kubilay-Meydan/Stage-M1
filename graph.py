import os
import pandas as pd
import matplotlib.pyplot as plt

# Couleurs pour les camemberts
pie_chart_colors = [
    "#BF7BA7ff",  # magenta-ciel
    "#F5C9C2ff",  # rose-thé
    "#FDF1E8ff",  # lin
    "#FEC7E3ff",  # conte-de-fée
    "#C699A6ff",  # puce
    "#323644ff",  # gris-acier
    "#ABBCE1ff",  # bleu-poudre
    "#E9E3E8ff",  # magnolia
    "#F0D5D4ff",  # rose-brume
    "#BF87CCff"   # violet-africain
]

def histogramme_ratio():
    # Définir les chemins
    complete_files_folder = "results"
    bips_files_folder = "results/BIPS"
    output_folder = "figures/ratio_genes_bips"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Obtenir la liste des fichiers complets et des fichiers BIPs
    complete_files = [f for f in os.listdir(complete_files_folder)]
    bips_files = [f for f in os.listdir(bips_files_folder) if f.startswith('BIP-')]

    ratios = []

    for bip_file in bips_files:
        # Trouver le fichier complet correspondant
        complete_file = bip_file[4:]

        if complete_file in complete_files:
            # Lire les fichiers
            bip_df = pd.read_csv(os.path.join(bips_files_folder, bip_file), sep='\t')
            complete_df = pd.read_csv(os.path.join(complete_files_folder, complete_file), sep='\t')

            # Calculer le ratio du nombre de lignes
            ratio = (len(bip_df) * 2) / len(complete_df)
            print(ratio)
            ratios.append(ratio)

    # Créer l'histogramme des ratios
    plt.hist(ratios, bins=10, color="#BF7BA7ff", edgecolor='white')
    plt.xlabel("Ratio du nombre de BIPs par rapport au nombre de gènes de l'espèce")
    plt.ylabel('Fréquence')
    plt.title('Histogramme du nombre de BIPs par rapport au nombre de gènes')
    plt.savefig("figures/ratio_genes_bips/histogramme_ratio.png")

def create_gene_type_pie_charts():
    bips_files_folder = "results/BIPS"
    output_folder = "figures/histogramme_type_gene_BIPs"
    mapping_csv_path = "summary+phylo.csv"

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lire le fichier CSV de correspondance
    mapping_df = pd.read_csv(mapping_csv_path)
    mapping_dict = mapping_df.set_index('id')['Species Name'].to_dict()

    # Obtenir la liste des fichiers BIPs
    bips_files = [f for f in os.listdir(bips_files_folder) if f.startswith('BIP-')]
    for bip_file in bips_files:
        bip_df = pd.read_csv(os.path.join(bips_files_folder, bip_file), sep='\t')

        # Obtenir l'ID du nom de fichier BIP
        bip_id = bip_file.split('_')[0][4:]  # Extraire le 'x' de 'BIP-x_...'

        # Obtenir le nom de l'espèce à partir du dictionnaire de correspondance
        species_name = mapping_dict.get(bip_id, bip_file)  # Valeur par défaut au bip_file si non trouvé

        # Obtenir les colonnes de type de gène
        gene_combinations = bip_df[['Gene type', 'Gene type']].apply(tuple, axis=1).value_counts()

        labels = [f'{combo[0]} & {combo[1]}' for combo in gene_combinations.index]
        sizes = gene_combinations.values
        total = sum(sizes)
        percentages = [f'{size/total*100:.1f}%' for size in sizes]
        legend_labels = [f'{label}: {percentage}' for label, percentage in zip(labels, percentages)]

        plt.figure(figsize=(15, 15))
        wedges, _ = plt.pie(sizes, startangle=140, colors=pie_chart_colors[:len(sizes)])

        plt.title(f'Combinaisons de types de gènes dans les BIPs de {species_name}')
        plt.axis('equal')  # Le rapport d'aspect égal assure que le camembert est dessiné en cercle.

        # Ajouter une légende ancrée dans le coin droit
        plt.legend(wedges, legend_labels, title="Combinaisons de Types de gènes", loc="upper left", bbox_to_anchor=(0.6, 0.6), fontsize='small')

        # Enregistrer le camembert en tant que fichier PNG
        output_path = os.path.join(output_folder, f'{species_name}_gene_type_pie_chart.png')
        plt.savefig(output_path)
        plt.close()

def create_chromosome_histograms():
    bips_files_folder = "results/BIPS"
    output_folder = "figures/histogramme_BIPs_par_chromosome"
    mapping_csv_path = "summary+phylo.csv"

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lire le fichier CSV de correspondance
    mapping_df = pd.read_csv(mapping_csv_path)
    mapping_dict = mapping_df.set_index('id')['Species Name'].to_dict()

    # Obtenir la liste des fichiers BIPs
    bips_files = [f for f in os.listdir(bips_files_folder) if f.startswith('BIP-')]
    for bip_file in bips_files:
        bip_df = pd.read_csv(os.path.join(bips_files_folder, bip_file), sep='\t')

        # Obtenir l'ID du nom de fichier BIP
        bip_id = bip_file.split('_')[0][4:]  # Extraire le 'x' de 'BIP-x_...'

        # Obtenir le nom de l'espèce à partir du dictionnaire de correspondance
        species_name = mapping_dict.get(bip_id, bip_file)  # Valeur par défaut au bip_file si non trouvé

        # Compter les occurrences de chaque nom de chromosome/échafaudage et les trier par nombre
        chromosome_counts = bip_df['Chromosome/scaffold name'].value_counts().sort_values(ascending=False)

        plt.figure(figsize=(10, 8))

        # Tracer les barres avec des positions spécifiques
        positions = range(len(chromosome_counts))
        plt.bar(positions, chromosome_counts.values, color=pie_chart_colors[:len(chromosome_counts)])

        # Définir les étiquettes des x-ticks et leurs positions
        plt.xticks(positions, chromosome_counts.index, rotation=90, ha='center')

        plt.xlabel('Chromosome')
        plt.ylabel('Nombre de BIPs')
        plt.title(f'Nombre de BIPs par chromosome chez {species_name}')

        # Enregistrer l'histogramme en tant que fichier PNG
        output_path = os.path.join(output_folder, f'{species_name}_chromosome_histogram.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()

def create_distance_histograms():
    bips_files_folder = "results/BIPS"
    output_folder = "figures/histogrammes_taille_BIPs"
    mapping_csv_path = "summary+phylo.csv"

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lire le fichier CSV de correspondance
    mapping_df = pd.read_csv(mapping_csv_path)
    mapping_dict = mapping_df.set_index('id')['Species Name'].to_dict()

    # Obtenir la liste des fichiers BIPs
    bips_files = [f for f in os.listdir(bips_files_folder) if f.startswith('BIP-')]
    for bip_file in bips_files:
        bip_df = pd.read_csv(os.path.join(bips_files_folder, bip_file), sep='\t')

        # Obtenir l'ID du nom de fichier BIP
        bip_id = bip_file.split('_')[0][4:]  # Extraire le 'x' de 'BIP-x_...'

        # Obtenir le nom de l'espèce à partir du dictionnaire de correspondance
        species_name = mapping_dict.get(bip_id, bip_file)  # Valeur par défaut au bip_file si non trouvé

        # Tracer l'histogramme pour la colonne "distance"
        plt.figure(figsize=(10, 8))
        plt.hist(bip_df['distance'], bins=30, color="#BF7BA7ff", edgecolor='white')

        plt.xlabel('Taille des BIPs (en pb)')
        plt.ylabel('Fréquence')
        plt.title(f'Taille des BIPs chez {species_name}')

        # Enregistrer l'histogramme en tant que fichier PNG
        output_path = os.path.join(output_folder, f'{species_name}_distance_histogram.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()

create_distance_histograms()
histogramme_ratio()
create_gene_type_pie_charts()
create_chromosome_histograms()
