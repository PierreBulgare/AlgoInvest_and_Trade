from algorithms.common import *
from itertools import combinations

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

def find_best_investment(data: pd.DataFrame)-> tuple:
    """
    Retourne la meilleure combinaison d'investissement

    Contraintes:
        - Chaque action ne peut être achetée qu'une seule fois
        - Impossible d'acheter une fraction d'action
        - Budget maximum de 500 €
    """
    best_combination = None
    best_profit = 0
    best_cost = 0

    for r in range(1, len(data) + 1):
        for combination in combinations(data.itertuples(index=False), r):
            total_cost = sum(action[1] for action in combination)
            total_profit = sum(action[3] for action in combination)
            
            if total_cost <= MAX_BUDGET and total_profit > best_profit:
                best_combination = combination
                best_profit = total_profit
                best_cost = total_cost
                
    return best_combination, best_profit, best_cost

def get_best_investment(file_path: str, output_file: str):
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