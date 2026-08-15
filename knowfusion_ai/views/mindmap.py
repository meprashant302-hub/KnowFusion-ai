import streamlit as st
from utils import auth, api_client
from utils.icons import icon_label

auth.require_auth()

st.markdown(icon_label("mindmap", "## Mind Map", size=26), unsafe_allow_html=True)
st.caption("Visualize how the concepts in a document connect to each other.")
st.write("")

sources = api_client.list_sources()
if not sources:
    st.info("No documents yet — upload one from the sidebar to get started.")
else:
    names = {s["name"]: s["id"] for s in sources}
    choice = st.selectbox("Choose a document", list(names.keys()))

    if st.button("Generate Mind Map", type="primary", icon=":material/auto_awesome:"):
        with st.spinner("Building mind map..."):
            result = api_client.generate_mind_map(names[choice])
        st.session_state["mindmap_data"] = result

    data = st.session_state.get("mindmap_data")
    if data:
        # Render as a Graphviz diagram when the graphviz package/binary is
        # available; otherwise fall back to a plain node/edge list so the
        # page never breaks in environments without Graphviz installed.
        try:
            dot_lines = [
                "digraph G {",
                'bgcolor="transparent"',
                'node [shape=box style="rounded,filled" fillcolor="#141A2A" fontcolor="#E5E7EB" color="#3B82F6"]',
                'edge [color="#3B82F6" fontcolor="#94A3B8"]',
            ]
            for n in data["nodes"]:
                dot_lines.append(f'"{n["id"]}" [label="{n["label"]}"]')
            for e in data["edges"]:
                label = f' [label="{e["label"]}"]' if e.get("label") else ""
                dot_lines.append(f'"{e["source"]}" -> "{e["target"]}"{label}')
            dot_lines.append("}")
            st.graphviz_chart("\n".join(dot_lines))
        except Exception:
            st.warning("Graphviz not available in this environment — showing raw structure instead.")
            st.write("**Nodes:**", [n["label"] for n in data["nodes"]])
            st.write("**Connections:**")
            id_to_label = {n["id"]: n["label"] for n in data["nodes"]}
            for e in data["edges"]:
                st.write(f"- {id_to_label[e['source']]} -> {id_to_label[e['target']]} ({e.get('label', '')})")
