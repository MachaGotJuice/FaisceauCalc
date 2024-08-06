import streamlit as st
import chardet
import os
from csv_to_graph import *
from nodes_to_distance import *
from csv_to_nodes import *
from nodes_to_csv import *

# Variables globales pour stocker les chemins des fichiers
graphe = ''
noeuds = ''

def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    file.seek(0)
    return encoding

def handle_file_upload_graphe(file):
    global graphe
    graphe = os.path.join(os.path.dirname(__file__),file.name)
    encoding = detect_encoding(file) or 'utf-8'  # Use 'utf-8' as a default encoding if detection fails
    try:
        content = file.read().decode(encoding)
        
    except UnicodeDecodeError:
        encoding = 'latin-1'  # Fallback to 'latin-1' if 'utf-8' fails
        content = file.read().decode(encoding)
    st.session_state['graphe_content'] = content
    st.session_state['graphe_filename'] = file.name

def handle_file_upload_noeuds(file):
    global noeuds
    noeuds = os.path.join(os.path.dirname(__file__), file.name)
    encoding = detect_encoding(file) or 'utf-8'  # Use 'utf-8' as a default encoding if detection fails
    try:
        content = file.read().decode(encoding)
    except UnicodeDecodeError:
        encoding = 'latin-1'  # Fallback to 'latin-1' if 'utf-8' fails
        content = file.read().decode(encoding)
    st.session_state['noeuds_content'] = content
    st.session_state['noeuds_filename'] = file.name

def on_poursuivre_click():
    global noeuds
    global graphe

    G = lire_excel_en_triplets(graphe)
    liste_noeuds = lire_couples_excel(noeuds)
    distances = []
    for i in range(len(liste_noeuds)):
        node1 = liste_noeuds[i][0]
        node2 = liste_noeuds[i][1]
        distances.append(calculate_distance(G, node1, node2))
    completer_colonne_excel(noeuds, distances)
    st.success('Distances calculées et fichier mis à jour!')

def main_page():
    st.title('Application de calcul de distance')
    
    st.subheader('Veuillez sélectionner votre graphe au format xslx ou csv:')
    graphe_file = st.file_uploader("Upload Graphe", type=["csv", "xlsx"], key='graphe')
    if graphe_file is not None:
        handle_file_upload_graphe(graphe_file)
        st.text_area('Contenu du fichier Graphe', st.session_state.get('graphe_content', ''), height=200, disabled=True)
    
    st.subheader('Veuillez sélectionner la liste des couples de noeuds au format xslx ou csv:')
    noeuds_file = st.file_uploader("Upload Noeuds", type=["csv", "xlsx"], key='noeuds')
    if noeuds_file is not None:
        handle_file_upload_noeuds(noeuds_file)
        st.text_area('Contenu du fichier Noeuds', st.session_state.get('noeuds_content', ''), height=200, disabled=True)
    
    if st.button('Poursuivre'):
        on_poursuivre_click()

if __name__ == "__main__":
    main_page()
