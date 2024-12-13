import pandas as pd

MAX_BUDGET = 500

def get_csv_datas(file_path: str)-> pd.DataFrame:
    """.
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

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        # Enregistre la meilleure combinaison
        best_combination_data.to_csv(f, index=False)

        # Ajoute une nouvelle ligne avec le total du coût et du bénéfice
        f.write(f"\nTotal (Coût/Bénéfice),{best_cost:.2f} €,,{best_profit:.2f} €")