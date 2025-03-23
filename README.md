# Projet de Chatbot avec OpenAI, LangChain, FastAPI et Streamlit

## Description
Ce projet implémente un chatbot interactif utilisant les modèles de langage d'OpenAI, LangChain pour l'orchestration des IA, FastAPI pour les services backend et Streamlit pour l'interface utilisateur. Le chatbot est conçu pour fournir un résumé d'un .txt, puis pour répondre  à toutes les questions qui suivent gardant en mémoire l'historique conversationnel.

## Fonctionnalités 
- Traitement automatique des langues basé sur les modèles GPT d'OpenAI
- Gestion efficace des flux de travail IA avec LangChain
- API RESTful backend utilisant FastAPI
- Interface utilisateur conviviale construite avec Streamlit
- Flux de conversation et base de connaissances personnalisables

## Installation
### Cloner le dépôt :

```bash
git clone https://github.com/Guiguishop/ChatAI.git
cd ChatAI
```

### Installer les dépendances :

```bash
pyenv install 3.9
pyenv local 3.9
poetry env use $(pyenv which python)
poetry install --no-root
eval $(poetry env activate)
```

### Configurer les variables d'environnement :
Créer un fichier .env à la racine du projet et ajouter votre clé API OpenAI, le model gpt utilisé (lhttps://platform.openai.com/docs/models) et la température du modèle :

```python
OPENAI_API_KEY=votre_clé_api_ici
OPENAI_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.2
```

## Utilisation

### Lancement du Backend FastAPI : 

```bash
uvicorn src.api.main:app --reload
```
L'API sera disponible à http://localhost:8000

### Lancement de l'Interface Streamlit :

```bash
streamlit run ./src/streamlit/app.py
```
Ouvrir votre navigateur et accéder à l'URL fournie par Streamlit (généralement http://localhost:8501)

## Structure du Projet

```text
ChatAI/
├── data/
│   ├── toto.txt
│   ├── titi.txt
├── notebooks/
│   ├── langchain.ipynb
│   ├── openai.ipynb
├── src/ 
│   ├── api
|   |   ├── __init__.py
|   |   ├── chain.py
|   |   ├── main.py
|   |   ├── prompts.py
│   ├── streamlit
|   |   ├── __init__.py
|   |   ├── app.py
├── test/
│   ├── test_api_functions.py 
├── .python-version
├── poetry.lock
├── pyproject.toml
├── .env
└── README.md
```

## Configuration
- Personnaliser les fichiers dans ./src/api/ pour ajuster les points de terminaison FastAPI (main.py) et l'intégration LangChain (chain.py / prompts.py)
- Modifier ./stc/streamlit/app.py pour changer l'interface utilisateur et les interactions avec le chatbot