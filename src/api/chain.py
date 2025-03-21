from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import MessagesState, END
from dotenv import load_dotenv
from src.api.prompts import PROMPT_SUMMARIZE, SYSTEM_PROMPT
from typing import Literal
import os

env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
)
load_dotenv(env_path)


class State(MessagesState):
    history: str


def summarize(conversation):
    prompt_template = PROMPT_SUMMARIZE
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["OPENAI_MODEL"],
        temperature=os.environ["TEMPERATURE"],
    )
    chain = prompt | llm | StrOutputParser()

    return chain.invoke(conversation)


def call_model(state: State, conversation_summary: str) -> dict:
    """
    Calls the language model to generate a response based on the current state and conversation summary.
    Args :
        state (State): The current state of the conversation, including history and messages.
        conversation_summary (str): A summary of the conversation so far.
    Returns:
        dict: A dictionnary containing the generated response message
    """

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["OPENAI_MODEL"],
        temperature=os.environ["TEMPERATURE"],
    )

    # If a summary exists, we add this in as a system message
    history = state.get("history", "")
    if history:
        system_message = f"Summary of conversation earlier: {history}"
        messages = [SystemMessage(content=system_message)] + state["messages"]

    else:  # Prompt "initial" de base qui va définir l'état de mon chatbot si pas de summary
        system_message = SYSTEM_PROMPT.format(conversation=conversation_summary)
        messages = [SystemMessage(content=system_message)] + state["messages"]

    response = llm.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# A compléter si on veut rajouter des étapes
def should_continue(state: State) -> Literal["summarize_history", END]:
    message = state["messages"]
    if len(message) > 6:
        return "summarize_history"
    return END


def summarize_history(state: State) -> dict:
    # S'il y a un historique conversationnel, cette fonction va le résumer

    llm_summarize = ChatOpenAI(
        temperature=os.environ["TEMPERATURE"],
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model=os.environ["OPENAI_MODEL"],
    )

    # Enregistre un historique conversationnel et dans l'historique, on supprime le message qu'il y avait dedans
    history = state.get("history", "")
    if history:
        history_message = f"Summary of conversation earlier: {history}"
    else:
        history_message = "No conversation history available"

    message = state["messages"] + [HumanMessage(content=history_message)]
    response = llm_summarize.invoke(message)

    delete_message = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"history": response.content, "messages": delete_message}


def print_update(update: dict) -> None:
    # Cette fonction permet d'afficher la réponse
    for k, v in update.items():  # Différentes conversations qu'on a
        for m in v["messages"]:
            m.pretty_print()
        if "history" in v:
            print(v["history"])
