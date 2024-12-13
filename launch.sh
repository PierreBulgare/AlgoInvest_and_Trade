#!/bin/bash

# Vérifie si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python n'est pas installé sur votre ordinateur. Veuillez installer Python."
    exit 1
fi

# Crée un environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "[INFO] Création de l'environnement virtuel..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Échec de la création de l'environnement virtuel."
        exit 1
    fi
fi

# Active l'environnement virtuel
echo "[INFO] Activation de l'environnement virtuel..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERREUR] Impossible d'activer l'environnement virtuel."
    exit 1
fi

# Vérifie si pip est installé dans l'environnement virtuel
if ! venv/bin/python -m pip --version &> /dev/null; then
    echo "[ERREUR] Pip n'est pas installé dans l'environnement virtuel."
    deactivate
    exit 1
fi

# Mise à jour de pip
echo "[INFO] Mise à jour de pip..."
venv/bin/python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "[ERREUR] Échec de la mise à jour de pip."
    deactivate
    exit 1
fi

# Installation des packages à partir de requirements.txt
if [ -f "requirements.txt" ]; then
    echo "[INFO] Installation des packages depuis requirements.txt..."
    venv/bin/python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Échec de l'installation des packages depuis requirements.txt."
        deactivate
        exit 1
    fi
else
    echo "[INFO] Aucun fichier requirements.txt trouvé. Ignoré."
fi

# Vérifie si main.py existe avant de l'exécuter
if [ ! -f "main.py" ]; then
    echo "[ERREUR] Le fichier main.py est introuvable."
    deactivate
    exit 1
fi

# Lance le fichier main.py
echo "[INFO] Lancement du programme..."
venv/bin/python main.py
if [ $? -ne 0 ]; then
    echo "[ERREUR] Le programme a rencontré une erreur."
    deactivate
    exit 1
fi

# Désactive l'environnement virtuel
deactivate

# Pause
echo "[INFO] Script terminé. Appuyez sur une touche pour fermer."
read -n 1 -s