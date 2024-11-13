import streamlit as st
import random
import time
from func import *

LNG = 'en'

# Add custom CSS to center the title
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    
    .header {
        text-align: center;
        font-size: 3rem; 
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .center-text {
                text-align: center;
            }
    </style>
    """,
    unsafe_allow_html=True
)

# Use st.markdown with custom CSS class instead of st.title to center it
st.markdown("<h1 class='title'>Welcome to CookBook Chat Bot</h1>", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.header("Menu")
    page = st.radio("Navigation", ["Main Chat", "Settings", "About"])

# Handling each page content
if page == "Main Chat":
    # Show bot description if no messages yet
    if "messages" not in st.session_state or not st.session_state.messages:
        intro_header = """<div class="center-text">Welcome to the CookBook Chat Bot! This bot is here to assist you with recipe ideas, 
answer general cooking questions, and help you modify recipes to suit your preferences. 
Here’s how to make the most out of your experience with this bot:</div>
        
#### Step-by-Step Instructions
1. Starting the Conversation (by sending a greeting message e.g., "Hello," "Hi there!").
2. Provide Your List of Ingredients (e.g., "I have chicken, onion, tomato, pasta...")
3. Request Modifications or Additional Recipes(e.g., "Can I make this gluten-free?" or "What if I don't have eggs?") or request more recipes if you want additional options.
4. Discuss Recipe Adjustments and Tips

#### Important Usage Notes
- Data Privacy: To protect your privacy, do not share personal or sensitive information with the bot. Keep your questions focused on recipes, cooking techniques, or ingredients only.
- Development Notice: Please be aware that this chatbot is still in the development stage. While it strives to provide accurate and helpful information, there may be occasional limitations or inconsistencies in responses.
        """
            
        if LNG == 'ru':
            intro_header = translate(context=intro_header, html=True, to_lang='ru')
        
        st.markdown(f"{intro_header}", unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(message["parts"][0])

    # Accept user input
    if prompt := st.chat_input("Type to get the recipe..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        
        # Determine which function to use based on message count
        if len(st.session_state.messages) >= 4:
            response_generator_func = stream_chatting
        elif len(st.session_state.messages) >= 2:
            response_generator_func = stream_get_first_recipes
        else:
            response_generator_func = stream_get_gemini_greeting_response
        
        # Stream assistant's response and display it
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator_func(user_input=prompt, context=st.session_state.messages))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "model", "parts": [response]})

elif page == "Settings":
    # Language setting for model responses
    st.header("Settings")
    st.warning("Still in the development")

elif page == "About":
    # Links to GitHub and LinkedIn
    st.header("About")
    st.write("This chat bot was created to assist users with recipe suggestions and general questions.")
    st.write("Connect with me:")
    st.markdown("- [GitHub](https://github.com/AlexRaudvee)")
    st.markdown("- [LinkedIn](https://www.linkedin.com/in/aleksandr-raudvee-aaab6b285/)")
