import os
import sys
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

# Ajout de la racine du projet au chemin de recherche
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from src.api.chain import State, summarize, call_model, summarize_history, should_continue, print_update

chain = None
app = FastAPI()


# Exemple d'un pointeur API
@app.get("/")
async def root():
    return "Hello World"


# Deuxième pointeur API
@app.post("/summarize")
async def summarize_text(file: UploadFile = File(...)):
    # Vérification si le fichier en entrée est un .txt
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()

    text = content.decode("utf-8")
    summary = summarize(text)

    return {"summary": summary}

# Pointeur API initialisant la chaîne conversationnelle
@app.post("/initialize")
async def initialize(file: UploadFile = File(...)):
    
    global chain # Variable globale
    
    # Vérification si le fichier en entrée est un .txt
    if file.content_type != "text/plain":
        return {"error": "Only text files are supported"}
    content = await file.read()

    text = content.decode("utf-8")
    
    # Define a new graph
    workflow = StateGraph(state_schema=State)
    workflow.add_node(
        "conversation",lambda input: call_model(state=input, conversation_summary=summary))
    workflow.add_node(summarize_history)
    workflow.add_edge(START, "conversation")
    workflow.add_conditional_edges(
        "conversation",
        should_continue,
    )
    workflow.add_edge("summarize_history", END)

    memory = MemorySaver()
    chain = workflow.compile(checkpointer=memory)
    
    summary = summarize(text)

    return {"summarize": summary}

async def generate_stream(input_message, config, chain):
    for event in chain.stream({"messages": [input_message]}, config, stream_mode = "updates"):
        yield event['conversation']['messages'][0].content # Envoie le contenu de l'événement au fur et à mesure

# Pointeur API gérant la conversation (traiter l'affichage du chat)
@app.post("/update")
async def update(request:str = Form(...)):
    config = {"configurable": {"thread_id": "4"}}

    input_message = HumanMessage(content=request)
    return StreamingResponse(generate_stream(input_message,config, chain), media_type = "text/plain")

    


# Chaque URL va exécuter tel ou tel fonction définit dans le pointeur API pouvant utiliser des fonctions
# python à l'intérieur


