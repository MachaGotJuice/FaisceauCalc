from csv_to_graph import * 
from nodes_to_distance import * 
from csv_to_nodes import *
from nodes_to_csv import * 

def logique():
    graphe = '/Users/salimelouahdani/Desktop/test.xlsx'
    noeuds = '/Users/salimelouahdani/Desktop/test copie.xlsx'

    G = lire_excel_en_triplets(graphe)
    liste_noeuds = lire_couples_excel(noeuds)
    distances = []
    print(liste_noeuds)
    for i in range(len(liste_noeuds)):
        node1 = liste_noeuds[i][0]
        node2 = liste_noeuds[i][1]
        distances.append(calculate_distance(G,node1,node2))
    print(distances)
    completer_colonne_excel(noeuds, distances)

logique()