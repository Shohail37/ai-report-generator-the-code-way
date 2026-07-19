import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file.")
    return LLM(
        model="openai/llama-3.1-8b-instant",
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
        temperature=0.3,
    )