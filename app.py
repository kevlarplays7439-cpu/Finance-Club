import streamlit as st

st.set_page_config(page_title="Finance Tug of War", layout="wide")

st.title("Finance Tug of War Quiz")

# ---------- GLOBAL GAME STATE ----------

if "question_bank" not in st.session_state:
    st.session_state.question_bank = None

if "used_questions" not in st.session_state:
    st.session_state.used_questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "responses" not in st.session_state:
    st.session_state.responses = []

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "rope_position" not in st.session_state:
    st.session_state.rope_position = 50   # 0 left win, 100 right win

st.info("Use sidebar to open Admin or Player panel")
