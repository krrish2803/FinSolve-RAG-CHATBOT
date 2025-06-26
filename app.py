import streamlit as st
import requests



st.title("FinSolve RAG Chatbot")

if "role" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state.get("logged_in"):
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{API_BASE}/login", json={"email": email, "password": password})
        if res.status_code == 200:
            st.session_state["logged_in"] = True
            st.session_state["role"] = res.json()["role"]
            st.success(f"Logged in as {st.session_state['role']}")
        else:
            st.error("Login failed")

else:
    query = st.text_input("Ask a question")
    if st.button("Submit") and query:
        res = requests.post(f"{API_BASE}/query", json={"query": query, "role": st.session_state["role"]})
        if res.status_code == 200:
            st.write("### Answer")
            st.markdown(res.json()["answer"])
            st.markdown("**Sources:** " + ", ".join(res.json()["sources"]))
        else:
            st.error("Error getting response")
