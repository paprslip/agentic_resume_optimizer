from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

openai = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

gemma3 = ChatOllama(
    model="gemma3",
    temperature=0.0,
    max_tokens=2048,
    top_p=0.95,
    top_k=40
)
llama3p2 = ChatOllama(
    model="llama3.2",
    temperature=0.0,
    max_tokens=2048,
    top_p=0.95,
    top_k=40
)
llama3p1 = ChatOllama(
    model="llama3.1",
    temperature=0.0,
    max_tokens=2048,
    top_p=0.95,
    top_k=40
)
deepseek_r1 = ChatOllama(
    model="deepseek-r1",
    temperature=0.0,
    max_tokens=2048,
    top_p=0.95,
    top_k=40
)