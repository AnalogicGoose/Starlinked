import streamlit as st
import openai
from streamlit_chat import message
import time
import os

# Streamlit page configuration
st.set_page_config(
    page_title="BarbAI:StarLinked",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load OpenAI API key
openai.api_key = st.secrets["OPENAIAPI_KEY"]

# Custom CSS for background and shooting stars
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://path-to-your-starry-night-image.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }
    [data-testid="stAppViewContainer"] .main {
        background-color: rgba(0,0,0,0);
    }
    .shooting-star {
        position: absolute;
        width: 3px;
        height: 3px;
        background: white;
        border-radius: 50%;
        animation: shoot 2s ease-out infinite;
    }
    @keyframes shoot {
        0% {opacity: 1; transform: translate(0, 0);}    
        100% {opacity: 0; transform: translate(500px, -300px);}    
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Place several shooting stars dynamically
for i in range(5):
    st.markdown(
        f"<div class='shooting-star' style='top:{i*10}vh; left:{i*20}vw; animation-delay:{i}s;'></div>",
        unsafe_allow_html=True
    )

# Title and description
st.title("🌌 BarbAI:StarLinked")
st.write("Preguntame cualquier cosa sobre los planetas y sus órbitas, basado en las leyes de Kepler!")

# Session state for chat history
def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

init_state()

# Prefab questions in sidebar
st.sidebar.header("Preguntas rápidas")
prefab_qs = [
    "Cual es el periodo orbital de Marte?",
    "Calcula la velocidad orbital de la Tierra en perihelio.",
    "Explica la tercera ley de Kepler.",
    "Cual es el eje semi-mayor de Júpiter?",
    "Cual es la distancia entre la Tierra y el Sol?",
]
for q in prefab_qs:
    if st.sidebar.button(q):
        st.session_state.user_input = q

# User input field
user_input = st.text_input("Tu pregunta:", st.session_state.user_input)

# Handle submission
if st.button("Mandar") and user_input:
    st.session_state.history.append(("user", user_input))
    with st.spinner("Thinking..."):
        # Use the new ChatCompletion API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=500,
            temperature=0
        )
        answer = response.choices[0].message["content"].strip()
        st.session_state.history.append(("ai", answer))
        st.session_state.user_input = ""

# Display chat history
for sender, text in st.session_state.history:
    if sender == "user":
        message(text, is_user=True)
    else:
        message(text)

# Suggestions for improvement:
# - Embed local orbital-mechanics calculations (e.g. via Astropy) to reduce API calls.
# - Cache responses with st.cache_data to speed up repeated queries.
# - Add interactive orbit visualizations with Plotly or matplotlib.
# - Provide dropdowns for planet selection and parameter presets.
# - Explore voice I/O with SpeechRecognition and st.audio components.
