import csv

def insert_into_tree(tree, path, species_name):
    # Navigate through the tree according to the path, creating dictionaries as needed
    for node in path:
        if node not in tree:
            tree[node] = {}
        tree = tree[node]
    # At the end of the path, place the species name
    tree[species_name] = {}

def tree_to_newick(tree):
    # Base case: if the tree is empty, return an empty string
    if not tree:
        return ''
    
    # Recursive case: build the Newick string for subtrees
    subtrees = []
    for node, subtree in tree.items():
        if subtree:  # Non-terminal node
            subtrees.append(f'({tree_to_newick(subtree)}){node}')
        else:  # Terminal node
            subtrees.append(node)
    
    return ','.join(subtrees)

# Initialize the root of the tree
phylo_tree = {}

# Read the CSV file and populate the tree
with open('summary+phylo.csv', mode='r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        species_name = row[0].strip()
        phylogeny = row[-1].strip().split(';')
        # Insert this species' phylogeny into the tree
        insert_into_tree(phylo_tree, [x.strip() for x in phylogeny], species_name)

# Convert the tree to Newick format
newick_representation = tree_to_newick(phylo_tree) + ';'

# Define the output file path
output_file_path = 'phylogeny.nw'

# Write the Newick representation to the output file
with open(output_file_path, 'w') as file:
    file.write(newick_representation)

print(f"Phylogenetic tree with species names saved in Newick format to {output_file_path}")
