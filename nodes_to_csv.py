import pandas as pd

def completer_colonne_excel(filepath, liste_nombres):
    """
    Complète une troisième colonne d'un fichier Excel avec les données d'une liste.
    
    Args:
    - filepath (str): Chemin vers le fichier Excel d'entrée.
    - liste_nombres (list): Liste de nombres à ajouter comme troisième colonne.
    """
    try:
        # Lire le fichier Excel
        df = pd.read_excel(filepath)
        
        # Vérifier si le fichier contient au moins deux colonnes
        if df.shape[1] < 2:
            raise ValueError("Le fichier doit contenir au moins deux colonnes.")
        
        # Vérifier si la longueur de la liste correspond au nombre de lignes du DataFrame
        if len(liste_nombres) != len(df):
            raise ValueError("La longueur de la liste ne correspond pas au nombre de lignes du fichier Excel.")
        
        # Ajouter la liste comme troisième colonne sans nom de colonne
        df.insert(loc=2, column='', value=liste_nombres)
        
        # Sauvegarder le fichier Excel complété
        df.to_excel(filepath, index=False, header=False)
        print(f"Fichier Excel complété sauvegardé sous {filepath}")
    
    except Exception as e:
        print(f"Erreur : {e}")

