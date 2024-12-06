import pandas as pd

def get_profit(action_cost, percentage):
    """Calcule le bénéfice en euros (en 2 ans)"""
    return round(action_cost * (percentage / 100) * 2, 2)

def get_csv_datas(file_path):
    """Récupère les données du CSV"""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
    except pd.errors.EmptyDataError:
        raise ValueError("Erreur : Le fichier est vide.")

def get_actions_datas(actions_data):
    """Récupère, convertit et retourne les données du CSV"""
    # Vérification de la présence des colonnes requises
    required_columns = ["Actions #", "Coût par action (en euros)", "Bénéfice (après 2 ans)"]
    if not all(col in actions_data.columns for col in required_columns):
        raise ValueError(f"Le fichier CSV doit contenir les colonnes suivantes : {required_columns}")
    
    # Conversion des données numériques en décimales
    actions_data["Bénéfice (après 2 ans)"] = actions_data["Bénéfice (après 2 ans)"].str.rstrip("%").astype(float)
    actions_data["Coût par action (en euros)"] = actions_data["Coût par action (en euros)"].astype(float)
    
    actions_data["Bénéfice (en euros)"] = actions_data.apply(
        lambda x: get_profit(x["Coût par action (en euros)"], x["Bénéfice (après 2 ans)"]),
        axis=1
    )
    return actions_data

def find_best_investment(data, budget=500):
    """
    Retourne la meilleure combinaison de manière optimisée
    """
    # Conversion des données en listes
    costs = data["Coût par action (en euros)"].tolist()
    profits = data["Bénéfice (en euros)"].tolist()
    n = len(costs)

    # Création d'une liste pour stocker les valeurs maximales
    max_values = [0] * (budget + 1)
    item_selection = [None] * (budget + 1)

    for i in range(n):
        for j in range(budget, int(costs[i]) - 1, -1):
            if max_values[j - int(costs[i])] + profits[i] > max_values[j]:
                max_values[j] = max_values[j - int(costs[i])] + profits[i]
                item_selection[j] = i

    # Création de la liste de la meilleur combinaison d'investissement
    best_combination = []
    # Stockage du budget de départ dans une nouvelle variable modifiable
    current_fund = budget
    while current_fund > 0 and item_selection[current_fund] is not None:
        i = item_selection[current_fund]
        best_combination.append(data.iloc[i])
        current_fund -= int(costs[i])

    total_profit = round(max_values[budget], 2)
    
    return pd.DataFrame(best_combination), total_profit

def save_best_investment(best_combination, best_profit, output_file):
    """Sauvegarde la meilleure combinaison dans un fichier CSV"""
    best_combination['Total Bénéfice'] = best_profit
    best_combination.to_csv(output_file, index=False)

def get_best_investment_optimized(file_path, output_file, budget=500):
    """Fonction principale"""
    csv_datas = get_csv_datas(file_path)
    if csv_datas is not None:
        actions_datas = get_actions_datas(csv_datas)
        best_combination, best_profit = find_best_investment(actions_datas, budget)
        save_best_investment(best_combination, best_profit, output_file)