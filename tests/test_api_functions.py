import os
import sys

# Ajout de la racine du projet au chemin de recherche
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


## 1- Test de la fonction qui résume le contenu d'un fichier
from src.api.chain import summarize

histoire_horde_path = os.path.join(
    os.path.dirname(os.getcwd()), "data", "histoire_horde.txt"
)

with open(histoire_horde_path, "r") as fichier:
    contenu = fichier.read()

summary = summarize(contenu)
print(summary)

## 2- Test des fonctions call_model, summarize_history, print_update et de la communication avec l'IA
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from src.api.chain import State, call_model, summarize_history, should_continue, print_update


# Define a new graph
workflow = StateGraph(state_schema=State)

# Define the conversation node and the summarize node
workflow.add_node(
    "conversation",lambda input: call_model(state=input, conversation_summary=summary))
workflow.add_node(summarize_history)

# Set the entrypoint as conversation
workflow.add_edge(START, "conversation")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `conversation`.
    # This means these are the edges taken after the `conversation` node is called.
    "conversation",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# We now add a normal edge  from `summarize_conversation` to END.
# This means that after `summarize_conversation` is called, we end?
workflow.add_edge("summarize_history", END)

# Finally, we compile it !
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Envoie de messages au bot prenant en compte l'historique conversationnel
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "4"}}

input_message = HumanMessage(content="Qui sont les principaux ennemis de la horde ?")
input_message.pretty_print()
for event in app.stream({"messages": [input_message]}, config, stream_mode="updates"):
    print_update(event)

input_message = HumanMessage(content="Parmi eux qui ont une épée ?")
input_message.pretty_print()
for event in app.stream({"messages": [input_message]}, config, stream_mode="updates"):
    print_update(event)
    
input_message = HumanMessage(content="Parle moi de l'histoire de cet homme ?")
input_message.pretty_print()
for event in app.stream({"messages": [input_message]}, config, stream_mode="updates"):
    print_update(event)
