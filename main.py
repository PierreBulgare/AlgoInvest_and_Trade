from algorythms.bruteforce import get_best_investment

def main():
    file_path = "liste_actions.csv"
    output_file_path = "datas/meilleur_combinaison.csv"
    get_best_investment(file_path, output_file_path)

if __name__ == "__main__":
    main()