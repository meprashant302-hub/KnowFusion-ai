import streamlit as st
from utils import auth, api_client
from utils.icons import icon_label

auth.require_auth()

st.markdown(icon_label("quiz", "## Generate Quiz", size=26), unsafe_allow_html=True)
st.caption("Turn any document into a quick self-test.")
st.write("")

sources = api_client.list_sources()
if not sources:
    st.info("No documents yet — upload one from the sidebar to get started.")
else:
    names = {s["name"]: s["id"] for s in sources}
    choice = st.selectbox("Choose a document", list(names.keys()))
    n = st.slider("Number of questions", 3, 10, 5)

    if st.button("Generate Quiz", type="primary", icon=":material/auto_awesome:"):
        with st.spinner("Generating quiz..."):
            result = api_client.generate_quiz(names[choice], num_questions=n)
        st.session_state["quiz_data"] = result["questions"]

    if "quiz_data" in st.session_state:
        for i, q in enumerate(st.session_state["quiz_data"], start=1):
            with st.container(border=True):
                st.markdown(f"**Q{i}. {q['question']}**")
                ans = st.radio("Options", q["options"], key=f"quiz_{i}", label_visibility="collapsed")
                if st.button("Check answer", key=f"check_{i}"):
                    if ans == q["options"][q["correct_index"]]:
                        st.success("Correct! " + q["explanation"])
                    else:
                        st.error("Not quite. " + q["explanation"])
