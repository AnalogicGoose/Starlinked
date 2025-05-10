import base64
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
encoded_key = os.getenv("OPENAIAPI_KEY_B64", st.secrets.get("OPENAIAPI_KEY", ""))
if not encoded_key:
    st.error("No se encontró la variable OPENAIAPI_KEY_B64 ni OPENAIAPI_KEY en secrets.")
    st.stop()
try:
    openai.api_key = base64.b64decode(encoded_key).decode("utf-8")
except Exception as e:
    st.error(f"Error al decodificar la API key: {e}")
    st.stop()
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
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}]
        )

        if response.choices and response.choices[0].message:
            answer = response.choices[0].message.content.strip()
        else:
            answer = "No se recibió respuesta válida."

        st.session_state.history.append(("assistant", answer))


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
