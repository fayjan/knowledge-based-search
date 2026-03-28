import streamlit as st
import requests

st.set_page_config(page_title="Knowledge Based Search", layout="wide")
st.title("📂 Knowledge Based Search (RAG)")

# Sidebar for file uploads
with st.sidebar:
    st.header("1. Document Ingestion")
    files = st.file_uploader("Upload PDF Documents", type="pdf", accept_multiple_files=True)
    if st.button("Process & Index"):
        if files:
            upload_data = [("files", (f.name, f.getvalue(), "application/pdf")) for f in files]
            res = requests.post("http://localhost:8000/ingest", files=upload_data)
            st.success(res.json()["message"])
        else:
            st.warning("Please upload files first.")

# Main chat logic
st.header("2. Search & Synthesis")
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API call to backend
    response = requests.post("http://localhost:8000/search", json={"query": prompt})
    answer = response.json()["answer"]

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    