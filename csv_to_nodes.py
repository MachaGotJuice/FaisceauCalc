import pandas as pd

def lire_couples_excel(filepath):
    """
    Lit un fichier Excel contenant deux colonnes et renvoie une liste de couples.
    
    Args:
    - filepath (str): Chemin vers le fichier Excel.
    
    Returns:
    - list: Liste de tuples contenant les données des deux colonnes.
    """
    try:
        df = pd.read_excel(filepath)
        
        # Vérifier si le fichier contient exactement deux colonnes
        if df.shape[1] != 2:
            raise ValueError("Le fichier doit contenir exactement deux colonnes.")
        
        # Convertir les données en une liste de tuples
        couples = list(df.itertuples(index=False, name=None))
        
        return couples
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return []
