import os
from crewai import LLM

MODEL_NAME = "groq/openai/gpt-oss-120b"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def make_llm(max_tokens=1200):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to Streamlit Cloud Secrets.")
    return LLM(model=MODEL_NAME, api_key=GROQ_API_KEY, temperature=0.1, max_tokens=max_tokens)
