import streamlit as st
from transformers import pipeline, Conversation
import time

owner = st.sidebar.header("Mohammed Rayan")
about = st.sidebar.subheader("About Us")
detail = st.sidebar.text("My Own ChatBot")

device = st.sidebar.selectbox("Select CPU/GPU",("cpu","cuda"))
audio = st.sidebar.selectbox("Get Audio Output?",("Yes","No"))

about_bot = st.sidebar.caption("__demo bot__")
chatllm = pipeline(task="conversational", model="facebook/blenderbot-400M-distill", device=device)

if audio == "Yes":
    audiollm = pipeline(task="text-to-speech", model="facebook/mms-tts-eng", device=device)

system_propmt = """You are a helpful AI chatbot that responds in friendly manner"""
chat_history = Conversation([{"role":"system","content": system_propmt}])

#chat session
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("type your prompt here"):
    with st.chat_message("user"):
        st.markdown(prompt)
        user_chat = {"role": "user", "content": prompt}
        chat_history.add_message(user_chat)
        # st.session_state.message.append(user_chat)
    try:
        response = chatllm(chat_history,max_length=1024)
    except:
        error_message = "You Exceeded Limit"
        with st.chat_message("assistant"):
            st.markdown(error_message)
        exit()
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_responce = ""
        assistant_responce = response.messages[-1]["content"]
        if audio == "Yes":
            audio_response = audiollm(assistant_responce)
        for chunk in assistant_responce.split():
            full_responce +=chunk + " "
            time.sleep(0.1)
            
            message_placeholder.markdown(full_responce + "| ")
        message_placeholder.markdown(full_responce)
        if audio == "Yes":
            st.audio(audio_response["audio"], sample_rate=audio_response["sampling_rate"])
        st.session_state.messages.append({"role":"assistant", "content":response.messages[-1]["content"]})
        
        
#to run streamlit run filename(chatbot.py)
