import time
import algorithms.bruteforce as bruteforce_algo
import algorithms.optimized as optimized_algo

def main():
    file_path = "liste_actions.csv"
    output_file_path = "datas/meilleur_combinaison.csv"

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
                    if algo_choice == 1:
                        # Calcul du temps d'exécution de bruteforce.py
                        print("Exécution de bruteforce.py ...")
                        start_time = time.time()
                        bruteforce_algo.get_best_investment(file_path, output_file_path)
                        bruteforce_execution_duration = time.time() - start_time
                        print(f"Bruteforce : {bruteforce_execution_duration:.3f} secondes")
                    elif algo_choice == 2:
                        # Calcul du temps d'exécution de optimized.py
                        print("Exécution de optimized.py ...")
                        start_time = time.time()
                        optimized_algo.get_best_investment(file_path, output_file_path)
                        optimized_execution_duration = time.time() - start_time
                        print(f"Optimized : {optimized_execution_duration:.3f} secondes")
                    else:
                        break
            else:
                print("Vous devez choisir entre 1, 2 et 3.")
        else:
            print("Vous devez entrer un chiffre.")

if __name__ == "__main__":
    main()