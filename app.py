import streamlit as st
import os
from prompt_engine import build_dog_prompt
from dotenv import load_dotenv
import requests
from streamlit_extras.stylable_container import stylable_container

# Load API key
load_dotenv()

# Local fallback image
DEFAULT_IMAGE = "IMG_9647.jpeg"

st.set_page_config(page_title="Just So You Know, Hooman", layout="wide")

# CSS styles
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fffdf7 !important;
        color: #2e2e2e !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.4rem;
    }
            
    .chat-bubble {
        margin-top: 1.5rem;
        background-color: #f9f1f0;
        padding: 1.2rem;
        border-radius: 1rem;
        color: #333;
        font-size: 1.2rem;
    }

    img {
        border-radius: 50%;
        width: 180px;
        height: 180px;
        object-fit: cover;
        margin-bottom: 1rem;
    }

    input, textarea {
        background-color: #ffffff !important;
        color: #2e2e2e !important;
        border: 1px solid #ccc !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
    }

    button[kind="primary"] {
        background-color: #E2725B !important;
        color: white !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 0.5rem 1.5rem !important;
        margin-top: 1rem;
    }

    button[kind="primary"]:hover {
        background-color: #cf6046 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<h2 style='text-align: center;'>Just So You Know, Hooman </h2>
<h6 style='text-align: center;'>(Ask your dog anything. They’ve got opinions!)</h6>
""", unsafe_allow_html=True)

# Layout
left, right = st.columns([1, 2], gap="large")

# LEFT: Profile card (entire form inside sage box)
with left:
    with stylable_container(
        key="green_container",
        css_styles="""
        {
            height: 800px;
            background-color: #e1ecd9;
            padding: 20px; # Optional: add some padding
            border-radius: 10px; # Optional: round the corners
        }
        """,
    ):
        dog_name = st.text_input("Name", value="Casper", key="dog_name")
        dog_breed = st.text_input("Breed", value="White German Shepherd", key="dog_breed")
        dog_traits = st.text_area("Personality Traits", value="playful, loyal, goofy, drama-queen", key="dog_traits")
        dog_photo_url = st.text_input("Dog Photo URL (optional)", "", key="dog_photo_url")
        if dog_photo_url:
            st.image(dog_photo_url)
        else:
            st.image(DEFAULT_IMAGE)

# RIGHT: Ask area (entire interaction in coral box)
with right:
    with stylable_container(
        key="terracotta_container",
        css_styles="""
        {
            height: 800px;
            background-color: #fbe6dc;
            padding: 20px; # Optional: add some padding
            border-radius: 10px; # Optional: round the corners
        }
        """,
    ):
        st.markdown("#### Ask your dog something:")
        user_input = st.text_input(" ", placeholder="Why do you bark at the neighbors?", key="user_input", label_visibility="collapsed")
        ask_button = st.button("Ask", key="ask_button", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

        if ask_button and user_input:
                with st.spinner("Your dog is thinking... 🐾"):
                    try:
                        prompt = build_dog_prompt(dog_name, dog_breed, dog_traits, user_input)
                        reply = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                                "HTTP-Referer": "https://just-so-you-know-human.local",
                                "X-Title": "Just So You Know, Human"
                            },
                            json={
                                "model": "deepseek/deepseek-chat-v3",
                                "messages": [{"role": "user", "content": prompt}]
                            }
                        )
                        if reply.status_code == 200:
                            content = reply.json()["choices"][0]["message"]["content"].strip()
                            st.markdown(f"<div class='chat-bubble'><strong>{dog_name} 🐶:</strong><br>{content}</div>", unsafe_allow_html=True)
                        else:
                            st.error("Something went wrong. Please try again.")
                    except Exception as e:
                        st.error(f"Error: {e}")
