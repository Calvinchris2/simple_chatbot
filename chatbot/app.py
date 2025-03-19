import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

system_prompt = "talk in tamil"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def list_available_models():
    try:
        available_models = genai.list_models()
        model_names = [model.name for model in available_models]
        return model_names
    except Exception as e:
        st.error(f"Error listing models: {e}")
        return []

def get_gemini_response(prompt, chat_history=None):
    try:
        # Added system_prompt while creating the model
        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=system_prompt)
        
        if chat_history:
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt)
        else:
            response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# Main app interface
def main():
    st.title("Gemini AI Chatbot")
    
    initialize_session_state()
    
    with st.sidebar:
        st.subheader("Information")
        if st.button("List Available Models"):
            models = list_available_models()
            st.write("Available models:")
            for model in models:
                st.write(f"- {model}")
    
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.write(content)

    user_input = st.chat_input("Ask me anything...")
    
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        formatted_history = []
        
        with st.spinner("Thinking..."):
            response = get_gemini_response(user_input)
        
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
