# Load necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables (for API key)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

# Start the chat with system instructions to act as a therapist
chat = model.start_chat(
    history=[], 
  
)

# Define a system message that acts as the instruction for the therapy bot
system_message = ("You are a professional therapist. "
                  "Answer only mental health and therapy-related questions with empathy and understanding. "
                  "If the question is not related to therapy, politely inform the user."
                  "You are a professional therapist who provides empathetic and supportive responses. "
                  "Instead of giving generic advice, you ask thoughtful questions to understand the user's feelings, "
                  "validate their emotions, and help them explore ways to cope with their challenges. "
                  "Respond like a therapist offering emotional support and guidance in a compassionate way."
                  )

def get_gemini_response(question):
    
    # Prepend the system message to ensure therapy focus
    full_prompt = f"{system_message}\nUser: {question}\nTherapist:"
    
    # Send the user question and get the response from Gemini Pro
    response = chat.send_message(full_prompt, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Therapy Chatbot", layout="wide")



# Custom styling for the chat layout.
st.markdown(
    """
    <style>
     .center-header {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .input-container input {
            flex-grow: 1;
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #ccc;
            margin-right: 10px;
        }
        # .input-container button {
        #     padding: 10px 20px;
        #     border-radius: 10px;
        #     background-color: #4CAF50;
        #     color: white;
        #     border: none;
        #     cursor: pointer;
        #     margin-left: -40px;
        # }
     
        .input-container button:hover {
            background-color: #45a049;
        }
        # .stButton{
        #   margin-top:10%;  
        #   margin-left: -40%;  
        # }
    .chat-container {
      
        border-radius: 10px;
        padding: 10px;
        max-height: 500px;
        overflow-y: auto;
    }
    .chat-message {
        margin: 5px 0;
    }
    .user-message {
        background-color: #8f9779;
        text-align: right;
        color: white;
        min-width:0;
    }
    .bot-message {
        background-color: #f0f0f5;
        text-align: left;
        color: #ccc;
        min-width:0;
    }
    </style>
    """, unsafe_allow_html=True
)
# Display the header in the center
st.markdown('<div class="center-header">Dr. Dizan Therapy Chatbot</div>', unsafe_allow_html=True)

# Container for chat history and input field
chat_container = st.container()
input_container = st.container()

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input

    
    st.markdown('<div class="input-container" style="display: flex; align-items: center;">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1]) 
with col1:   
    input = st.text_input("What is bothering you? ", key="input")
with col2:    
    submit = st.button("Send")
    st.markdown('</div>', unsafe_allow_html=True)
    

# When the user submits the question
if submit and input:
    # Get the response from Gemini Pro API
    response = get_gemini_response(input)
    
    # Add user query to chat history
    st.session_state['chat_history'].append(("You", input))
    
    # Stream the AI response in chunks and add to chat history
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    st.session_state['chat_history'].append(("Bot", response_text))

# Display Chat History
with chat_container:
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.markdown(f'<div class="chat-message user-message">Patient: {text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">Bot: {text}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)   

