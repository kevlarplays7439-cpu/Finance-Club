import streamlit as st

st.title("Answer Question")

# ---------- SHOW TUG OF WAR ----------

st.subheader("Tug of War")
st.progress(st.session_state.rope_position)

team = st.text_input("Enter Team Name")

if st.session_state.current_question is not None:

    q = st.session_state.current_question

    st.subheader(q["Question"])

    answer = st.radio(
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
                st.error("Team already submitted")
            else:
                st.session_state.responses.append({
                    "team": team,
                    "answer": answer
                })
                st.success("Answer submitted")

else:
    st.info("Waiting for admin to start question")
