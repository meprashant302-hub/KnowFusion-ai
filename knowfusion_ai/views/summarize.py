import streamlit as st
from utils import auth, api_client
from utils.icons import icon_label

auth.require_auth()

st.markdown(icon_label("document", "## Summarize Document", size=26), unsafe_allow_html=True)
st.caption("Pick a document from your knowledge base and generate an AI summary.")
st.write("")

sources = api_client.list_sources()
if not sources:
    st.info("No documents yet — upload one from the sidebar to get started.")
else:
    names = {s["name"]: s["id"] for s in sources}
    choice = st.selectbox("Choose a document", list(names.keys()))
    length = st.select_slider("Summary length", options=["Brief", "Standard", "Detailed"], value="Standard")

    if st.button("Generate Summary", type="primary", icon=":material/auto_awesome:"):
        with st.spinner("Summarizing..."):
            result = api_client.summarize_document(names[choice])
        with st.container(border=True):
            st.markdown(result["summary"])
