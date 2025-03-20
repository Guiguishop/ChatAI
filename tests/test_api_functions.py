import os
import sys

# Ajout de la racine du projet au chemin de recherche
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from src.api.chain import summarize


## Test de la fonction summarize dans chain.py
histoire_horde_path = os.path.join(
    os.path.dirname(os.getcwd()), "data", "histoire_horde.txt"
)

with open(histoire_horde_path, "r") as fichier:
    contenu = fichier.read()

summarize(contenu)
