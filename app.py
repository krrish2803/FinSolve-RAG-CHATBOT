import streamlit as st
import requests

API_BASE = "API_BASE = "http://localhost:8000"

st.set_page_config(page_title="FinSolve RAG Chatbot", layout="centered")
st.title("🤖 FinSolve RAG Chatbot")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None

# Login section
if not st.session_state["logged_in"]:
    st.subheader("🔐 Login to Continue")
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("Login"):
        try:
            res = requests.post(f"{API_BASE}/login", json={"email": email, "password": password})
            if res.status_code == 200:
                data = res.json()
                st.session_state["logged_in"] = True
                st.session_state["role"] = data.get("role", "user")
                st.success(f"✅ Logged in as **{st.session_state['role']}**")
            else:
                st.error("❌ Login failed. Please check your credentials.")
        except Exception as e:
            st.error(f"🚨 Server error: {e}")

# Chatbot section
else:
    st.success(f"Welcome, **{st.session_state['role']}**")
    st.markdown("---")
    query = st.text_input("💬 Ask a question:", placeholder="e.g. What is TDS on salary?")

    if st.button("Submit") and query.strip():
        try:
            payload = {
                "query": query.strip(),
                "role": st.session_state["role"]
            }
            res = requests.post(f"{API_BASE}/query", json=payload)
            if res.status_code == 200:
                result = res.json()
                st.markdown("### ✅ Answer")
                st.markdown(result.get("answer", "No answer provided."))

                sources = result.get("sources", [])
                if sources:
                    st.markdown(f"**Sources:** {', '.join(sources)}")
            else:
                st.error("❌ Error: Could not fetch a response from the backend.")
        except Exception as e:
            st.error(f"🚨 Server error: {e}")

