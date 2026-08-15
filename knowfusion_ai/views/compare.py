import streamlit as st
from utils import auth, api_client
from utils.icons import icon_label

auth.require_auth()

st.markdown(icon_label("compare", "## Compare Documents", size=26), unsafe_allow_html=True)
st.caption("Select two or more documents to see an AI-generated comparison.")
st.write("")

sources = api_client.list_sources()
if len(sources) < 2:
    st.info("Upload at least two documents to use comparison.")
else:
    names = {s["name"]: s["id"] for s in sources}
    picked = st.multiselect("Choose documents to compare", list(names.keys()))

    if st.button("Compare", type="primary", disabled=len(picked) < 2, icon=":material/auto_awesome:"):
        with st.spinner("Comparing..."):
            result = api_client.compare_documents([names[p] for p in picked])
        with st.container(border=True):
            st.markdown(result["comparison"])
