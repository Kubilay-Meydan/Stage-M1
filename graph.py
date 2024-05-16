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
    output_folder = "figures/diagrammes_circulaires_Type_BIPS"
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

        # Obtenir les colonnes de types de gènes (colonne 8 et colonne 16)
        gene_type1 = bip_df.iloc[:, 7]  # 8ème colonne (index 7)
        gene_type2 = bip_df.iloc[:, 15] # 16ème colonne (index 15)

        # Classifier les combinaisons de types de gènes
        def classify_gene_type(type1, type2):
            if type1 == 'protein_coding' and type2 == 'protein_coding':
                return 'protein_coding & protein_coding'
            elif type1 == 'protein_coding' or type2 == 'protein_coding':
                return 'protein_coding & other'
            else:
                return 'other & other'

        # Appliquer la classification
        gene_combinations = [classify_gene_type(type1, type2) for type1, type2 in zip(gene_type1, gene_type2)]
        gene_combinations = pd.Series(gene_combinations).value_counts()

        labels = gene_combinations.index
        sizes = gene_combinations.values
        total = sum(sizes)
        percentages = [f'{size/total*100:.1f}%' for size in sizes]
        legend_labels = [f'{label}: {percentage}' for label, percentage in zip(labels, percentages)]

        plt.figure(figsize=(15, 15))
        wedges, _ = plt.pie(sizes, startangle=140, colors=pie_chart_colors[:len(sizes)])

        plt.title(f'Combinaisons de types de gènes dans les BIPs de {species_name}')
        plt.axis('equal')  # Le rapport d'aspect égal assure que le camembert est dessiné en cercle.

        # Ajouter une légende ancrée dans le coin droit
        plt.legend(wedges, legend_labels, title="Combinaisons de Types de gènes", loc="upper left", bbox_to_anchor=(0.6, 0.5), fontsize='medium')

        # Enregistrer le camembert en tant que fichier PNG
        output_path = os.path.join(output_folder, f'{species_name}_gene_type_pie_chart.png')
        plt.savefig(output_path)
        plt.close()

def create_chromosome_histograms():
    complete_files_folder = "results"
    bips_files_folder = "results/BIPS"
    output_folder = "figures/histogrammes_genes_et_BIPs_par_chromosome"
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
        
        # Trouver le fichier complet correspondant
        complete_file = bip_file[4:]
        complete_df = pd.read_csv(os.path.join(complete_files_folder, complete_file), sep='\t')

        # Obtenir l'ID du nom de fichier BIP
        bip_id = bip_file.split('_')[0][4:]  # Extraire le 'x' de 'BIP-x_...'

        # Obtenir le nom de l'espèce à partir du dictionnaire de correspondance
        species_name = mapping_dict.get(bip_id, bip_file)  # Valeur par défaut au bip_file si non trouvé

        # Compter les occurrences de chaque nom de chromosome/échafaudage dans BIP et Complete files
        bip_chromosome_counts = bip_df['Chromosome/scaffold name'].value_counts()
        complete_chromosome_counts = complete_df['Chromosome/scaffold name'].value_counts()

        # Obtenir une liste unique de chromosomes/échafaudages
        all_chromosomes = list(set(bip_chromosome_counts.index).union(set(complete_chromosome_counts.index)))
        all_chromosomes.sort()

        bip_counts = bip_chromosome_counts.reindex(all_chromosomes, fill_value=0)
        complete_counts = complete_chromosome_counts.reindex(all_chromosomes, fill_value=0)

        x = range(len(all_chromosomes))  # Positions des barres

        plt.figure(figsize=(15, 8))

        # Largeur de chaque barre
        bar_width = 0.4

        # Tracer les barres pour les BIP files
        plt.bar(x, bip_counts.values, width=bar_width, color="#BF7BA7ff", label='Nombre de BIPs')

        # Tracer les barres pour les Complete files, décalées de bar_width
        plt.bar([p + bar_width for p in x], complete_counts.values, width=bar_width, color="#ABBCE1ff", label='Nombre de gènes')

        # Définir les étiquettes des x-ticks et leurs positions
        plt.xticks([p + bar_width / 2 for p in x], all_chromosomes, rotation=90, ha='center')

        plt.xlabel('Chromosome')
        plt.ylabel('Nombre de BIPs / Genes')
        plt.title(f'Nombre de BIPs et Genes par chromosome chez {species_name}')

        # Ajouter la légende
        plt.legend()

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
