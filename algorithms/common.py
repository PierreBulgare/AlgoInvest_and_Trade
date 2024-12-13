import os
import pandas as pd
from typing import Callable

MAX_BUDGET = 500

def get_csv_datas(file_path: str) -> pd.DataFrame:
    """
    Lit et retourne le contenu du fichier CSV
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Erreur : Le fichier {file_path} est introuvable.")
    except pd.errors.EmptyDataError:
        raise ValueError("Erreur : Le fichier est vide.")

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données en supprimant les lignes avec des valeurs incorrectes ou absentes.
    Renomme les colonnes pour garantir un format standard.
    """
    if "name" in data.columns and "price" in data.columns and "profit" in data.columns:
        data = data.rename(columns={
            "name": "Actions #",
            "price": "Coût par action (en euros)",
            "profit": "Bénéfice (en euros)"
        })
        data["Bénéfice (après 2 ans)"] = (data["Bénéfice (en euros)"] / data["Coût par action (en euros)"]) * 100
    
    data["Coût par action (en euros)"] = pd.to_numeric(data["Coût par action (en euros)"], errors="coerce")
    data["Bénéfice (après 2 ans)"] = pd.to_numeric(data["Bénéfice (après 2 ans)"], errors="coerce")

    data = data.dropna(subset=["Coût par action (en euros)", "Bénéfice (après 2 ans)"])

    return data

def get_actions_datas(actions_data: pd.DataFrame) -> pd.DataFrame:
    """
    Récupère dynamiquement les données en fonction des colonnes disponibles.
    Gère un format standardisé :
    Actions #, Coût par action (en euros), Bénéfice (après 2 ans), Bénéfice (en euros)
    """
    data_frame = pd.DataFrame({
        "Actions #": actions_data["Actions #"],
        "Coût par action (en euros)": actions_data["Coût par action (en euros)"],
        "Bénéfice (après 2 ans)": actions_data["Bénéfice (après 2 ans)"],
        "Bénéfice (en euros)": get_profit(
            actions_data["Coût par action (en euros)"],
            actions_data["Bénéfice (après 2 ans)"]
        )
    })
    return data_frame

def get_profit(action_cost: pd.Series, profit_percentage: pd.Series) -> pd.Series:
    """
    Calcule le bénéfice en euros en fonction du coût et du pourcentage de bénéfice.

    Calcul : (Coût de l'action * Pourcentage de Bénéfice) / 100
    """
    return round(action_cost * (profit_percentage / 100), 2)

def save_best_investment(best_combination, best_profit, best_cost, actions_datas: pd.DataFrame, output_file: str):
    """
    Enregistre la meilleure combinaison d'investissement dans un fichier CSV
    """
    best_combination_data = pd.DataFrame(best_combination, columns=actions_datas.columns)

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        best_combination_data.to_csv(f, index=False)
        f.write(f"\nTotal (Coût/Bénéfice),{best_cost:.2f} €,,{best_profit:.2f} €")

def get_best_investment(file_path: str, output_file: str, find_best_investment: Callable):
    """
    Fonction principale
    """
    csv_datas = get_csv_datas(file_path)
    
    if csv_datas is not None:
        csv_datas = clean_data(csv_datas)
        actions_datas = get_actions_datas(csv_datas)
        best_combination, best_profit, best_cost = find_best_investment(actions_datas)
        save_best_investment(best_combination, best_profit, best_cost, actions_datas, output_file)