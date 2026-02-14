import streamlit as st
import pandas as pd
import random

st.set_page_config(layout="wide")
st.title("Finance Tug of War Quiz")

# ---------------- GAME STATE ----------------

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "responses" not in st.session_state:
    st.session_state.responses = []

if "used_questions" not in st.session_state:
    st.session_state.used_questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "question_active" not in st.session_state:
    st.session_state.question_active = False

if "last_winner" not in st.session_state:
    st.session_state.last_winner = None

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "question_bank" not in st.session_state:
    st.session_state.question_bank = None

# ---------------- MODE SELECT ----------------

mode = st.sidebar.selectbox("Select Mode", ["Admin", "Player"])

# ================= PLAYER PAGE =================

if mode == "Player":

    st.header("Join Quiz")

    team = st.text_input("Enter Team Name")

    if st.session_state.question_active and st.session_state.current_question is not None:

        q = st.session_state.current_question
        st.subheader(q["Question"])

        selected = st.radio(
            "Choose answer",
            [q["Option1"], q["Option2"], q["Option3"], q["Option4"]]
        )

        if st.button("Submit Answer"):

            if not team:
                st.warning("Enter team name")
            else:
                already_submitted = any(
                    r["team"] == team for r in st.session_state.responses
                )

                if already_submitted:
                    st.error("Your team already submitted")
                else:
                    st.session_state.responses.append({
                        "team": team,
                        "answer": selected
                    })
                    st.success("Answer submitted")

    else:
        st.info("Waiting for next question")

# ================= ADMIN PAGE =================

if mode == "Admin":

    st.header("Admin Control Panel")

    # -------- Upload Question File --------

    file = st.file_uploader("Upload Question Excel")

    if file:
        st.session_state.question_bank = pd.read_excel(file)
        st.success("Question bank loaded")

    df = st.session_state.question_bank

    # -------- Start Next Question --------

    if df is not None:

        available = df[~df["ID"].isin(st.session_state.used_questions)]

        st.write("Remaining Questions:", len(available))

        if st.button("Start Next Question"):

            if len(available) == 0:
                st.error("No questions left")
            else:
                q = available.sample(1).iloc[0]

                st.session_state.current_question = q
                st.session_state.used_questions.append(q["ID"])
                st.session_state.responses = []
                st.session_state.question_active = True

    # -------- Show Current Question --------

    if st.session_state.current_question is not None:

        q = st.session_state.current_question
        st.subheader("Current Question")
        st.write(q["Question"])

        st.write("Responses received:", len(st.session_state.responses))

        # -------- Show Result --------

        if st.button("Show Result"):

            st.session_state.question_active = False

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

                st.session_state.scores[winner] += int(q["Points"])

                # -------- 3 WIN STREAK RULE --------

                if winner == st.session_state.last_winner:
                    st.session_state.streak += 1
                else:
                    st.session_state.streak = 1
                    st.session_state.last_winner = winner

                st.success(f"Winner: {winner}")
                st.write("Win streak:", st.session_state.streak)

                if st.session_state.streak == 3:
                    st.balloons()
                    st.header(f"{winner} wins by 3 streak!")

    # -------- Leaderboard --------

    st.subheader("Leaderboard")

    if st.session_state.scores:
        leaderboard = pd.DataFrame(
            st.session_state.scores.items(),
            columns=["Team", "Score"]
        ).sort_values("Score", ascending=False)

        st.table(leaderboard)
    else:
        st.write("No scores yet")

    # -------- Reset Game --------

    if st.button("Reset Game"):

        st.session_state.scores = {}
        st.session_state.responses = []
        st.session_state.used_questions = []
        st.session_state.current_question = None
        st.session_state.last_winner = None
        st.session_state.streak = 0
        st.session_state.question_active = False

        st.success("Game reset")

