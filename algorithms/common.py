import os
import pandas as pd
from typing import Callable

MAX_BUDGET = 500

def get_csv_datas(file_path: str)-> pd.DataFrame:
    """
    Lit et retourne le contenu du fichier CSV
    """
    try:
        return pd.read_csv(file_path)
    # Gestion de l'erreur si le fichier est introuvable
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
    # Arrêt du programme si le fichier est vide
    except pd.errors.EmptyDataError:
        raise ValueError("Erreur : Le fichier est vide.")
    
def get_actions_datas(actions_data: pd.DataFrame)-> pd.DataFrame:
    """
    Récupère les données des actions présentes dans le fichier CSV

    Déroulement :
        - Vérification des colonnes requises
        - Création du DataFrame
        - Ajout d'une colonne "Bénéfiche (en euros)"
    """
    # Vérification de la présence des colonnes requises
    required_columns = ["Actions #", "Coût par action (en euros)", "Bénéfice (après 2 ans)"]

    # Arrêter le programme si toutes les colonnes ne sont pas présentes
    if not all(col in actions_data.columns for col in required_columns):
        raise ValueError(f"Le fichier CSV doit contenir les colonnes suivantes : {required_columns}")
    
    # Création du DataFrame et ajout de la colonne Bénéfice (en euros)
    data_frame = pd.DataFrame({
        'Actions #': actions_data["Actions #"],
        'Coût par action (en euros)': actions_data["Coût par action (en euros)"],
        'Bénéfice (après 2 ans)': actions_data["Bénéfice (après 2 ans)"],
        'Bénéfice (en euros)': get_profit(
            actions_data["Coût par action (en euros)"],
            actions_data["Bénéfice (après 2 ans)"].str.rstrip("%").astype(float)
        )
    })

    return data_frame

def get_profit(action_cost: float, profit_percentage: float)-> float:
    """
    Calcule le bénéfice (En Euros) (En 2 ans)

    Calcul :
        (Coût de l'action * Pourcentage de Bénéfice) * 2 ans
        (Résultat arrondi à deux décimales)
    """
    return round(action_cost * (profit_percentage / 100) * 2, 2)

def save_best_investment(best_combination, best_profit, best_cost, actions_datas: pd.DataFrame, output_file: str):
    """
    Enregistre la meilleure combinaison d'investisseemnt dans un fichier CSV
    """
    best_combination_data = pd.DataFrame(best_combination, columns=actions_datas.columns)

    output_dir = os.path.dirname(output_file)
    # Crée le dossier "datas/" s'il n'existe pas
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        # Enregistre la meilleure combinaison
        best_combination_data.to_csv(f, index=False)

        # Ajoute une nouvelle ligne avec le total du coût et du bénéfice
        f.write(f"\nTotal (Coût/Bénéfice),{best_cost:.2f} €,,{best_profit:.2f} €")

def get_best_investment(file_path: str, output_file: str, find_best_investment: Callable):
    """
    Fonction principale
    """
    # Récupère les données du CSV
    csv_datas = get_csv_datas(file_path)

    if csv_datas is not None:
        # Récupère les données des actions
        actions_datas = get_actions_datas(csv_datas)
        # Récupère la meilleure combinaison d'investissement
        best_combination, best_profit, best_cost = find_best_investment(actions_datas)
        # Sauvegarde la combinaison dans un fichier CSV
        save_best_investment(best_combination, best_profit, best_cost, actions_datas, output_file)