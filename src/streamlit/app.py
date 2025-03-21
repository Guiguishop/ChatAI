import streamlit as st
import requests

st.title("Chatbot of summarization")
st.header("Generate a summary of text with .txt file")

# Création d'une variable d'état de session pour stocker le résumé
if 'resume' not in st.session_state: 
    st.session_state.resume = None

upload_file = st.file_uploader("Upload a file",type = ["txt"])

if upload_file is not None:
    files = {'file': (upload_file.name, upload_file.read(), upload_file.type)}
    
    if st.button('Summarize'):
        response = requests.post('http://127.0.0.1:8000/initialize', files=files)
        if response.status_code == 200: # si le fichier a bien été lu
            st.session_state.resume = response.json().get("summarize") # stocke le résumé dans la session
        else:
            st.write("Error")

if st.session_state.resume:
    st.write("Summarization : ")
    st.write(st.session_state.resume)
    
    
    st.header("Chatbot")
    
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    user_input = st.chat_input("Enter your message here")
    if user_input:
        st.session_state.history.append({"role": "user", "content" : user_input})
        response = requests.post('http://127.0.0.1:8000/update', data  = {"request" : user_input}, stream= True)
        if response.status_code == 200:
            response_text = ""
            # Va ajouter dans la réponse les tokens qu'il reçoit au fur et à mesure en stream
            for token in response.iter_lines():
                if token:
                    response_text += token.decode('utf-8')
            st.session_state.history.append({"role" : "bot", "content" : response_text})
        else:
            st.write("Error")
    
    for message in st.session_state.history:
        if message["role"] == "user":
            st.write("You : " , message["content"])
        else:
            st.write("Bot : " , message["content"])
            
    