from algorithms.common import *
from itertools import combinations

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