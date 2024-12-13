from algorithms.common import *

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
                    dp_table[action_index - 1][current_budget]
                )
            else:
                dp_table[action_index][current_budget] = dp_table[action_index - 1][current_budget]

    # Récupération des actions sélectionnées
    selected_indices = []
    remaining_budget = MAX_BUDGET
    for action_index in range(total_actions, 0, -1):
        if dp_table[action_index][remaining_budget] != dp_table[action_index - 1][remaining_budget]:
            selected_indices.append(action_index - 1)
            remaining_budget -= round(action_costs[action_index - 1])

    # Construction du DataFrame final des actions sélectionnées
    selected_df = data.iloc[selected_indices].reset_index(drop=True)

    # Calcul des coûts et bénéfices
    total_cost = selected_df["Coût par action (en euros)"].sum()
    total_profit = round(dp_table[total_actions][MAX_BUDGET], 2)

    return selected_df, total_profit, total_cost