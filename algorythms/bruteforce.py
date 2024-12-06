import pandas as pd
from itertools import combinations

def get_profit(action_cost, percentage):
    """ Calcule le bénéfice en euros (en 2 ans) """
    return round(action_cost * (percentage / 100) * 2, 2)

def get_csv_datas(file_path):
    """Récupère les données du CSV"""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")

def get_actions_datas(actions_data):
    """ Récupère, convertit et retourne les données du CSV """
    # Vérification de la présence des colonnes requises
    required_columns = ["Actions #", "Coût par action (en euros)", "Bénéfice (après 2 ans)"]
    if not all(col in actions_data.columns for col in required_columns):
        raise ValueError(f"Le fichier CSV doit contenir les colonnes suivantes : {required_columns}")
    
    # Conversion des données numériques en décimales
    actions_data["Bénéfice (après 2 ans)"] = actions_data["Bénéfice (après 2 ans)"].str.rstrip("%").astype(float)
    actions_data["Coût par action (en euros)"] = actions_data["Coût par action (en euros)"].astype(float)
    
    # Création du DataFrame et ajout de la colonne Bénéfice (en euros)
    data_frame = pd.DataFrame({
        'Actions #': actions_data["Actions #"],
        'Coût par action (en euros)': actions_data["Coût par action (en euros)"],
        'Bénéfice (après 2 ans)': actions_data["Bénéfice (après 2 ans)"],
        'Bénéfice (en euros)': get_profit(
            actions_data["Coût par action (en euros)"],
            actions_data["Bénéfice (après 2 ans)"]
        )
    })
    return data_frame

def find_best_investment(data, budget=500):
    """
    Vérifie chaque combinaison d'investissements et retourne les meilleurs

    Conditions:
        - Chaque action ne peut être achetée qu'une seule fois
        - Impossible d'acheter une fraction d'action
        - Budget maximum de 500 €
    """
    best_combination = None
    best_profit = 0

    for r in range(1, len(data) + 1):
        for combination in combinations(data.itertuples(index=False), r):
            total_cost = sum(action[1] for action in combination)
            total_profit = sum(action[3] for action in combination)
            
            if total_cost <= budget and total_profit > best_profit:
                best_combination = combination
                best_profit = total_profit
                
    return best_combination, best_profit

def save_best_investment(best_combination, best_profit, actions_datas, output_file):
    """Sauvegarde la meilleure combinaison dans un fichier CSV"""
    best_combination_data = pd.DataFrame(best_combination, columns=actions_datas.columns)
    best_combination_data['Total Bénéfice'] = best_profit
    best_combination_data.to_csv(output_file, index=False)

def get_best_investment(file_path, output_file):
    """Fonction principale"""
    csv_datas = get_csv_datas(file_path)
    if csv_datas is not None:
        actions_datas = get_actions_datas(csv_datas)
        best_combination, best_profit = find_best_investment(actions_datas)
        save_best_investment(best_combination, best_profit, actions_datas, output_file)