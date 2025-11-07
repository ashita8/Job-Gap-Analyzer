from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

def get_tavily_client(api_key: str) -> TavilyClient:
    return TavilyClient(api_key=api_key)

def get_gemini_model(api_key: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
