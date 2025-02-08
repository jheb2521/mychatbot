import streamlit as st
import requests

# Function to send user input to the Flask backend
def send_to_backend(user_input):
    response = requests.post('http://localhost:5000/chat', json={'question': user_input, 'context': st.session_state.get('context', '')})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error: Unable to get response from backend.")
        return None

# Initialize session state variables
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'context' not in st.session_state:
    st.session_state.context = ''

# Main conversation interface
st.title("Chat Interface")

# Add custom CSS to set the width of the container
st.markdown(
    """
    <style>
    .chat-container {
        width: 250px;
        margin: auto;
    }
    .chat-message {
        padding: 10px;
        border-radius: 100px;
        margin-bottom: 15px;
    }
    .user-message {
        background-color: #007BFF;
        color: white;
        text-align: right;
    }
    .bot-message {
        background-color: #00000f;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a container for the chat interface
chat_container = st.container()

with chat_container:
    chat_placeholder = st.empty()
    with st.container():
        user_input = st.text_input("Type your message here...", key="user_input")
        if st.button("Send"):
            if user_input:
                # Send user input to the Flask backend
                backend_response = send_to_backend(user_input)
                if backend_response:
                    # Update conversation history
                    st.session_state.conversation_history.append(f"{user_input}")
                    st.session_state.conversation_history.append(f"Mentor: {backend_response['response']}")
                    st.session_state.context = backend_response['context']
                    st.rerun()

    # Display the conversation in a chat-like format
    with chat_placeholder.container():
        st.subheader("Conversation")
        for message in st.session_state.conversation_history:
            if message.startswith("You:"):
                st.markdown(f"<div class='chat-message user-message'>{message}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message bot-message'>{message}</div>", unsafe_allow_html=True)