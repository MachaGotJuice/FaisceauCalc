
import networkx as nx
def calculate_distance(G, node1, node2):
    graph = nx.Graph()
    graph.add_weighted_edges_from(G)
    try:
        distance = nx.shortest_path_length(graph, source=node1, target=node2, weight='weight')
        return distance
    except nx.NetworkXNoPath:
        return float('inf')  # Retourne l'infini si aucun chemin n'existe