import streamlit as st
import chardet
import os
import pandas as pd
import networkx as nx
from csv_to_graph import *
from nodes_to_distance import *

# Variable globale pour stocker le chemin du fichier de graphe
graphe = ''

def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    file.seek(0)
    return encoding

def handle_file_upload_graphe(file):
    global graphe
    graphe = os.path.join(os.path.dirname(__file__), file.name)
    encoding = detect_encoding(file) or 'utf-8'  # Utilise 'utf-8' comme encodage par défaut si la détection échoue
    try:
        content = file.read().decode(encoding)
    except UnicodeDecodeError:
        encoding = 'latin-1'  # Replis sur 'latin-1' si 'utf-8' échoue
        content = file.read().decode(encoding)
    st.session_state['graphe_content'] = content
    st.session_state['graphe_filename'] = file.name

def calculate_distances(df, G, margins):
    distances = []
    for index, row in df.iterrows():
        node1 = row['Départ']
        node2 = row['Arrivée']
        try:
            distance = nx.shortest_path_length(G, source=node1, target=node2, weight='weight')
            # Ajouter les marges des nœuds de départ et d'arrivée
            total_distance = distance + margins[node1] + margins[node2]
            distances.append(total_distance)
        except (nx.NetworkXNoPath, KeyError):
            distances.append("Noeud introuvable")  # Message d'erreur si le noeud n'est pas trouvé
    df['Longueur'] = distances

def generate_graph(triplets):
    G = nx.Graph()
    for (node1, node2, distance) in triplets:
        G.add_edge(node1, node2, weight=distance)
    return G

def main_page():
    st.title('Application de calcul de distance')
    
    st.subheader('Veuillez sélectionner votre graphe au format xslx ou csv:')
    graphe_file = st.file_uploader("Upload Graphe", type=["csv", "xlsx"], key='graphe')
    
    if graphe_file is not None:
        handle_file_upload_graphe(graphe_file)
        triplets = lire_excel_en_triplets(graphe)
        
        # Créer le graphe avec NetworkX
        G = generate_graph(triplets)
        nodes = list(G.nodes())

        # Tableau pour les marges des nœuds
        st.subheader('Tableau des marges des nœuds')
        margins_data = {
            "Nœuds": nodes,
            "Marges": [0] * len(nodes)  # Initialiser toutes les marges à 0
        }
        margins_df = pd.DataFrame(margins_data)

        # Permettre à l'utilisateur de modifier le tableau des marges
        edited_margins_df = st.data_editor(margins_df, num_rows="dynamic", use_container_width=True)

        # Convertir les marges modifiées en un dictionnaire
        margins_dict = pd.Series(edited_margins_df.Marges.values, index=edited_margins_df.Nœuds).to_dict()

        # Tableau modifiable à trois colonnes, initialement vide
        st.subheader('Tableau des itinéraires')
        st.write("Ajoutez des itinéraires ci-dessous :")
        data = {
            "Départ": pd.Series(dtype='str'),  # S'assurer que le type de colonne est une chaîne
            "Arrivée": pd.Series(dtype='str'),  # S'assurer que le type de colonne est une chaîne
            "Longueur": pd.Series(dtype='str')  # Initialiser avec chaîne pour gérer les erreurs
        }
        df = pd.DataFrame(data)

        # Permettre à l'utilisateur de modifier le tableau
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        if st.button('Calculer'):
            calculate_distances(edited_df, G, margins_dict)
            st.success('Distances calculées!')
            st.dataframe(edited_df, use_container_width=True)  # Afficher le dataframe mis à jour

    # Centrer le tableau
    st.markdown(
        """
        <style>
        [data-testid="stDataFrame"] div.stDataFrame {
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main_page()
