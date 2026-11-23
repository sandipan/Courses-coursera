# pip install langchain, langchain_openai

'''
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# Read OpenAI API key
with open("api_key", "r") as f:
    api_key = f.read().strip()

# Define tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4.1",
    api_key=api_key
)

# Create agent
agent = create_agent(
    model=llm,
    tools=[multiply],
    system_prompt="You are a helpful mathematical assistant."
)

# Invoke agent
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 25 times 40?"}
    ]
})

print(result["messages"][-1].content)
'''


from langchain.agents import create_agent
from langchain_ollama import ChatOllama

# Define tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Initialize local LLM
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Create agent
agent = create_agent(
    model=llm,
    tools=[multiply],
    system_prompt="You are a helpful mathematical assistant."
)

# Invoke agent
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 25 times 40?"}
    ]
})

print(result["messages"][-1].content)


import requests
import time
from functools import lru_cache
from langchain_core.tools import tool

API_URL = "https://en.wikipedia.org/w/api.php"

session = requests.Session()

# Replace with your actual contact email
session.headers.update({
    "User-Agent": "AI-Math-Assistant-Lab/1.0 (your-email@example.com)"
})

@lru_cache(maxsize=100)
def wikipedia_search(query: str) -> str:

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": 1,
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "format": "json",
        "maxlag": 5
    }

    for attempt in range(3):
        response = session.get(
            API_URL,
            params=params,
            timeout=20
        )

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 10))
            print(f"Rate limited. Waiting {wait} seconds...")
            time.sleep(wait)
            continue

        response.raise_for_status()

        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        if not pages:
            return "No relevant Wikipedia article found."

        page = next(iter(pages.values()))

        return page.get("extract", "No summary available.")

    return "Wikipedia API is currently rate-limiting requests. Please try again later."


@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for factual information about a topic."""
    return wikipedia_search(query)


# Test
result = search_wikipedia.invoke({
    "query": "What is tool calling?"
})

print(result)
