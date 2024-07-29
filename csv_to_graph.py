import pandas as pd

def lire_excel_en_triplets(nom_fichier):
    # Lire le fichier Excel
    df = pd.read_excel(nom_fichier, engine='openpyxl')
    
    # Vérifier si le fichier a exactement trois colonnes
    if df.shape[1] != 3:
        raise ValueError("Le fichier Excel doit contenir exactement trois colonnes")
    
    # Créer la liste des triplets
    triplets = []
    for index, row in df.iterrows():
        triplet = tuple(row)
        triplets.append(triplet)
    
    return triplets

