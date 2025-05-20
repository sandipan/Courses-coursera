import ollama
# pip install streamlit
import streamlit as st

if "model" not in st.session_state:
    st.session_state["model"] = "llama3:latest"

if "messages" not in st.session_state:
    st.session_state["messages"] = []


for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask your question"):
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state["messages"].append({"role": "user", "content": prompt})

    full_response = ""
    placeholder = st.empty()
    model = st.session_state["model"]
    for chunk in ollama.chat(
        model=model, messages=st.session_state["messages"], stream=True
    ):
        if chunk:
            full_response += chunk["message"]["content"]
            placeholder.markdown(full_response + "|")
        placeholder.markdown(full_response)
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
