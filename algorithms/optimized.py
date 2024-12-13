from algorithms.common import *

def get_actions_datas(actions_data: pd.DataFrame)-> pd.DataFrame:
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

def find_best_investment(data: pd.DataFrame) -> tuple:
    """
    Retourne la meilleure combinaison d'investissement

    Contraintes:
        - Chaque action ne peut être achetée qu'une seule fois
        - Impossible d'acheter une fraction d'action
        - Budget maximum de 500 €
    """

    # Extraction des colonnes coûts et bénéfices en liste
    action_costs = data["Coût par action (en euros)"].tolist()
    action_profits = data["Bénéfice (en euros)"].tolist()
    total_actions = len(action_costs)

    # Tableau de Programmation Dynamique pour stocker les bénéfices maximaux
    dp_table = [[0] * (MAX_BUDGET + 1) for _ in range(total_actions + 1)]

    # Mise à jour du Tableau de Programmation Dynamique
    for action_index in range(1, total_actions + 1):
        for current_budget in range(MAX_BUDGET + 1):
            action_cost = action_costs[action_index - 1]
            action_profit = action_profits[action_index - 1]
            
            if action_cost <= current_budget:
                dp_table[action_index][current_budget] = max(
                    action_profit + dp_table[action_index - 1][int(current_budget - action_cost)],
                    dp_table[action_index - 1][current_budget],
                )
            else:
                dp_table[action_index][current_budget] = dp_table[action_index - 1][current_budget]

    # Récupération des actions sélectionnées
    selected_actions = []
    remaining_budget = MAX_BUDGET
    for action_index in range(total_actions, 0, -1):
        if dp_table[action_index][remaining_budget] != dp_table[action_index - 1][remaining_budget]:
            selected_actions.append(data.iloc[action_index - 1])
            remaining_budget -= int(action_costs[action_index - 1])

    # Calcul des coûts et bénéfices
    total_cost = sum(action["Coût par action (en euros)"] for action in selected_actions)
    total_profit = round(dp_table[total_actions][MAX_BUDGET], 2)

    return pd.DataFrame(reversed(selected_actions)), total_profit, total_cost

def get_best_investment_optimized(file_path: str, output_file: str):
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