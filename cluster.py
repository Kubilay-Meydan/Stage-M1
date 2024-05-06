import os
import re
from Bio import Phylo
from scipy.cluster.hierarchy import linkage, fcluster
from collections import defaultdict

def extract_name_from_filename(filename):
    match = re.search(r'BIP-(\w+)_gene_ensembl', filename)
    if match:
        return match.group(1)
    return None

def read_newick_and_extract_distances(tree_path):
    tree = Phylo.read(tree_path, "newick")
    terminals = tree.get_terminals()
    distances = {terminal.name: {} for terminal in terminals}

    for terminal in terminals:
        for other in terminals:
            distances[terminal.name][other.name] = tree.distance(terminal, other)
    
    return distances, terminals

def cluster_files_in_families(directory, tree_path, num_clusters=20):
    distances, terminals = read_newick_and_extract_distances(tree_path)
    terminal_list = [t.name for t in terminals]
    dist_matrix = [[distances[name1][name2] for name2 in terminal_list] for name1 in terminal_list]

    # Perform hierarchical clustering
    Z = linkage(dist_matrix, 'average')
    clusters = fcluster(Z, num_clusters, criterion='maxclust')
    
    # Map names to clusters
    name_to_cluster = {name: cluster for name, cluster in zip(terminal_list, clusters)}
    
    # Create clusters for files
    file_clusters = defaultdict(list)
    other_files = []

    for filename in os.listdir(directory):
        if 'BIP-' in filename and filename.endswith('_gene_ensembl'):
            name = extract_name_from_filename(filename)
            if name and name in name_to_cluster:
                cluster_number = name_to_cluster[name]
                file_clusters[cluster_number].append(filename)
            else:
                other_files.append(filename)
    
    return file_clusters, other_files

# Example usage
directory_path = 'results/BIPS'
newick_file_path = 'taxonomy.nw'
file_clusters, others = cluster_files_in_families(directory_path, newick_file_path)
print(len(file_clusters.items()))
for cluster_id, files in file_clusters.items():
    print(f"Cluster {cluster_id}:")
    for file in files:
        print(f"  {file}")
print("Other files not in the Newick tree:")
for file in others:
    print(f"  {file}")
