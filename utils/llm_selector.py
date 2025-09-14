import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(provider: str):
    if provider == "openai":
        return ChatOpenAI(
            model="gpt-5-nano",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY")
        )
    else:
        raise ValueError("Unsupported provider. Use 'openai' or 'gemini'.")
