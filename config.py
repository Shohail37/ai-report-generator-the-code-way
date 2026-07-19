import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# On Streamlit Cloud, secrets come from st.secrets, not a .env file.
# This pulls them into the normal environment variables if needed.
try:
    import streamlit as st
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    if "SERPER_API_KEY" in st.secrets:
        os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
except Exception:
    pass

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file or Streamlit secrets.")
    return LLM(
        model="openai/llama-3.1-8b-instant",
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
        temperature=0.3,
    )