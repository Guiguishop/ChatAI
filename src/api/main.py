import os
import sys
from fastapi import FastAPI, UploadFile, File

# Ajout de la racine du projet au chemin de recherche
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from src.api.chain import summarize

app = FastAPI()


# Exemple d'un pointeur API
@app.get("/")
async def root():
    return "Hello World"


# Deuxième pointeur API
@app.post("/summarize")
async def summarize_text(file: UploadFile = File(...)):
    # Vérificatin si le fichier en entrée est un .txt
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()

    text = content.decode("utf-8")
    summary = summarize(text)

    return {"summary": summary}


# Chaque URL va exécuter tel ou tel fonction définit dans le pointeur API pouvant utiliser des fonctions
# python à l'intérieur
