from nicegui import ui
from csv_to_graph import * 
from nodes_to_distance import * 
from csv_to_nodes import *
from nodes_to_csv import * 
# Variables globales pour stocker les chemins des fichiers
graphe = ''
noeuds = ''

def handle_file_upload_graphe(file):
    global graphe
    graphe = file.name
    print(graphe)
    with open(file.name, 'r') as f:
        content = f.read()
        text_area_graphe.set_value(content)

def handle_file_upload_noeuds(file):
    global noeuds
    noeuds = file.name
    print('*************')
    print(file.name)
    print('************')
    with open(file.name, 'r') as f:
        content = f.read()
        text_area_noeuds.set_value(content)

def on_poursuivre_click():
    global noeuds
    global graphe

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

@ui.page('/')
def main_page():
    global text_area_graphe, text_area_noeuds

    ui.label('Veuillez sélectionner votre graphe au format xslx ou csv:')
    file_upload_graphe = ui.upload(on_upload=handle_file_upload_graphe)
    text_area_graphe = ui.textarea(label='Contenu du fichier Graphe').props('readonly')
    
    ui.label('Veuillez sélectionner la liste des couples de noeuds au format xslx ou csv:')
    file_upload_noeuds = ui.upload(on_upload=handle_file_upload_noeuds)
    text_area_noeuds = ui.textarea(label='Contenu du fichier noeuds').props('readonly')

    ui.button('Poursuivre', on_click=on_poursuivre_click)
    
    dark = ui.dark_mode()
    ui.label('Switch mode:')
    ui.button('Dark', on_click=dark.enable)
    ui.button('Light', on_click=dark.disable)

ui.run()
