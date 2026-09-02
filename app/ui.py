import os
import httpx
import streamlit as st

API_URL = os.getenv("DOCUMIND_API_URL", "http://localhost:8000")
st.set_page_config(page_title="DocuMind", page_icon="🧠", layout="wide")

st.title("🧠 DocuMind")
st.caption("Ask questions across your own documents, images, audio and video.")

with st.sidebar:
    st.header("Knowledge Library")
    files = st.file_uploader(
        "Add files", accept_multiple_files=True,
        type=["pdf","txt","md","csv","json","html","docx","pptx","xlsx","png","jpg","jpeg","webp","mp3","wav","m4a","mp4","mov","avi","webm"]
    )
    if st.button("Index selected files", use_container_width=True, disabled=not files):
        progress = st.progress(0)
        for i, uploaded in enumerate(files or []):
            with st.spinner(f"Indexing {uploaded.name}..."):
                response = httpx.post(f"{API_URL}/ingest", files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}, timeout=600)
                if response.is_success:
                    st.success(f"Indexed {uploaded.name}")
                else:
                    st.error(f"{uploaded.name}: {response.text}")
            progress.progress((i+1)/len(files))
    st.divider()
    try:
        sources = httpx.get(f"{API_URL}/sources", timeout=5).json()
        st.metric("Indexed sources", len(sources))
        for source in sources:
            st.caption(f"• {source['source_name']}  ·  {source['modality']}")
    except Exception:
        st.warning("Start the API on port 8000 to use DocuMind.")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources used"):
                for s in message["sources"]:
                    st.write(f"**{s['source']}** {s['locator']} · {s['modality']} · relevance {s['score']:.2f}")

if prompt := st.chat_input("Ask anything about the files you added..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching your knowledge library..."):
            try:
                r = httpx.post(f"{API_URL}/ask", json={"question": prompt}, timeout=180)
                r.raise_for_status(); data = r.json()
                st.markdown(data["answer"])
                if data.get("sources"):
                    with st.expander("Sources used"):
                        for s in data["sources"]:
                            st.write(f"**{s['source']}** {s['locator']} · {s['modality']} · relevance {s['score']:.2f}")
                st.session_state.messages.append({"role":"assistant","content":data["answer"],"sources":data.get("sources",[])})
            except Exception as exc:
                st.error(f"DocuMind could not answer: {exc}")
