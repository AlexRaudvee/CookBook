import streamlit as st
import random
import time
from func import *

# Add custom CSS to center the title
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .header {
        text-align: center;
        font-size: 3rem; 
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
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
        st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """            
            <div class="center-text">
                Welcome to the CookBook Chat Bot! This bot is here to assist you with recipe ideas, 
                answer general cooking questions, and help you modify recipes to suit your preferences. 
                Here’s how to make the most out of your experience with this bot:
            </div>
            
            #### Step-by-Step Instructions
            1. Starting the Conversation
                - Begin by sending a greeting message (e.g., "Hello," "Hi there!").
                - The bot will respond with its own greeting, introducing itself and preparing for the conversation.
            2. Provide Your List of Ingredients
                - After the initial greeting, the next message should be a list of ingredients you have on hand.
                - List each ingredient clearly, and avoid extra information for the best results. This allows the bot to suggest recipes that match your available ingredients.
            3. Request Recipes Based on Your Ingredients
                - Once the bot has your ingredients, ask it to provide a set of recipes that you can make. The bot is designed to give you options that vary in complexity, including:
                - One easy and fast recipe
                - One moderately challenging recipe
                - One vegan recipe (or a more complex option if a vegan recipe isn't possible with your ingredients)
            4. Request Modifications or Additional Recipes
                - After receiving recipes, you may ask the bot for modifications (e.g., "Can I make this gluten-free?" or "What if I don't have eggs?") or request more recipes if you want additional options.
            5. Discuss Recipe Adjustments and Tips
                - The bot can assist in adjusting recipes for dietary restrictions, ingredient swaps, and cooking methods. Use this function to discuss modifications or substitutions in detail.
                
            #### Important Usage Notes
                - Data Privacy: To protect your privacy, do not share personal or sensitive information with the bot. Keep your questions focused on recipes, cooking techniques, or ingredients only.
                - Development Notice: Please be aware that this chatbot is still in the development stage. While it strives to provide accurate and helpful information, there may be occasional limitations or inconsistencies in responses.
            """,
            unsafe_allow_html=True
        )
    
    # Streamed response emulator
    def response_generator():
        response = random.choice([
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?"
        ])
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

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
    st.selectbox("Choose Language:", ["English", "Spanish", "French"], key="language")

elif page == "About":
    # Links to GitHub and LinkedIn
    st.header("About")
    st.write("This chat bot was created to assist users with recipe suggestions and general questions.")
    st.write("Connect with me:")
    st.markdown("- [GitHub](https://github.com/your-profile)")
    st.markdown("- [LinkedIn](https://www.linkedin.com/in/your-profile)")
