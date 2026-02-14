import streamlit as st
import pandas as pd

st.title("Admin Control Panel")

# ---------- SHOW TUG OF WAR ----------

st.subheader("Tug of War Progress")
st.progress(st.session_state.rope_position)

# ---------- UPLOAD QUESTIONS ----------

file = st.file_uploader("Upload Question Excel (.xlsx or .csv)")

if file:
    if file.name.endswith(".csv"):
        st.session_state.question_bank = pd.read_csv(file)
    else:
        st.session_state.question_bank = pd.read_excel(file)

    st.success("Question bank loaded")

# ---------- START QUESTION ----------

if st.session_state.question_bank is not None:

    df = st.session_state.question_bank
    available = df[~df["ID"].isin(st.session_state.used_questions)]

    st.write("Remaining Questions:", len(available))

    if st.button("Start Next Question"):

        if len(available) > 0:
            q = available.sample(1).iloc[0]

            st.session_state.current_question = q
            st.session_state.used_questions.append(q["ID"])
            st.session_state.responses = []

        else:
            st.error("No questions left")

# ---------- SHOW CURRENT QUESTION ----------

if st.session_state.current_question is not None:

    q = st.session_state.current_question

    st.subheader("Current Question")
    st.write(q["Question"])

    st.write("Responses received:", len(st.session_state.responses))

    # ---------- CALCULATE RESULT ----------

    if st.button("Show Result"):

        result = {}

        for r in st.session_state.responses:
            team = r["team"]

            if team not in result:
                result[team] = {"correct": 0, "total": 0}

            result[team]["total"] += 1

            if r["answer"] == q["Answer"]:
                result[team]["correct"] += 1

        if len(result) == 0:
            st.warning("No responses received")

        else:

            accuracy = {
                t: result[t]["correct"] / result[t]["total"]
                for t in result
            }

            winner = max(accuracy, key=accuracy.get)

            if winner not in st.session_state.scores:
                st.session_state.scores[winner] = 0

            st.session_state.scores[winner] += 10

            # ---------- AUTO ROPE MOVEMENT ----------
            # Team A or Left moves left. Others move right.
            if winner.lower() in ["team a", "a", "left"]:
                st.session_state.rope_position -= 10
            else:
                st.session_state.rope_position += 10

            st.success("Winner: " + winner)

            if st.session_state.rope_position <= 0:
                st.error("LEFT SIDE WINS GAME")

            if st.session_state.rope_position >= 100:
                st.success("RIGHT SIDE WINS GAME")

# ---------- LEADERBOARD ----------

st.subheader("Leaderboard")

if st.session_state.scores:
    st.write(st.session_state.scores)
else:
    st.write("No scores yet")

# ---------- RESET GAME ----------

if st.button("Reset Game"):
    st.session_state.used_questions = []
    st.session_state.current_question = None
    st.session_state.responses = []
    st.session_state.scores = {}
    st.session_state.rope_position = 50
    st.success("Game reset")
