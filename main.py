import time
import algorithms.bruteforce as bruteforce_algo
import algorithms.optimized as optimized_algo
from algorithms.common import get_best_investment

def main():
    files = ["csv/liste_actions.csv", "csv/dataset_1.csv", "csv/dataset_2.csv"]
    while True:
        algo_choice = input(
                "===================================\n"
                "Quelle méthode voulez-vous tester ?\n"
                "1. Bruteforce\n"
                "2. Optimized\n"
                "3. Quitter\n"
                "Entrez votre choix : "
            )

        if algo_choice.isdigit():
            algo_choice = int(algo_choice)
            if algo_choice in [1, 2, 3]:
                for file in files:
                    output_file_path_bruteforce = f"datas/best_combinaison_bruteforce_{file.split("/")[1].strip(".csv")}.csv"
                    output_file_path_optimized = f"datas/best_combinaison_optimized_{file.split("/")[1].strip(".csv")}.csv"
                    if algo_choice == 1:
                        # Calcul du temps d'exécution de bruteforce.py
                        print("Exécution de bruteforce.py ...")
                        start_time = time.time()
                        get_best_investment(file, output_file_path_bruteforce, bruteforce_algo.find_best_investment)
                        bruteforce_execution_duration = time.time() - start_time
                        print(f"Bruteforce Algorithm Duration : {bruteforce_execution_duration:.3f} secondes")
                    elif algo_choice == 2:
                        # Calcul du temps d'exécution de optimized.py
                        print("Exécution de optimized.py ...")
                        start_time = time.time()
                        get_best_investment(file, output_file_path_optimized, optimized_algo.find_best_investment)
                        optimized_execution_duration = time.time() - start_time
                        print(f"Optimized Algorithm Duration : {optimized_execution_duration:.3f} secondes")
                    else:
                        break
            else:
                print("Vous devez choisir entre 1, 2 et 3.")
        else:
            print("Vous devez entrer un chiffre.")

if __name__ == "__main__":
    main()