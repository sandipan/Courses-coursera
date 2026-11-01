from google import genai
import os
import json
from google.genai import types


from dotenv import load_dotenv 

# Load variables from .env into the environment
load_dotenv()
# Configure the API key
#genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# The URL of the article to analyze
article_url = "https://developers.googleblog.com/en/new-gemini-api-updates-for-gemini-3/"

# (The article_schema defined in Step 2 must be available here)
# Define the required output structure for the article analysis
ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "key_takeaways": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3
        }
    },
    "required": ["title", "summary", "key_takeaways"]
}

# CREATE CLIENT (new google-genai style) 
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("FATAL ERROR: GEMINI_API_KEY environment variable not set.")
    raise SystemExit(1)
  
   # YOUR CODE HERE: Create Client Command

def _get_api_key() -> str:
    """
    Return an API key from env vars (GEMINI_API_KEY fallback).
    Raises if neither is set.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "Missing API key. Set GEMINI_API_KEY "
            "(e.g., export GEMINI_API_KEY='YOUR_KEY')"
        )
    return key


def _make_client() -> genai.Client:
    """
    Create a Google GenAI client for the Developer API.
    """
    return genai.Client(api_key=_get_api_key())


client = _make_client()


# --- FETCH ARTICLE SUMMARY USING URL CONTEXT (TOOLS) 
def fetch_article_summary(article_url: str) -> str:
    """
    Use URL Context to read the article and return a concise summary.
    This call uses tools, so we DO NOT request JSON here.
    """
    prompt = (
        # YOUR CODE HERE: Prompt the AI to use URL Context to read the article at the URL below.
        f'Read the article from here {article_url} and summarize'
    )

    # Make the generation request
    response = client.models.generate_content(
            model= 'gemini-3-flash-preview',
            contents=prompt,
            config={
                # Tools allowed here (URL Context)
                "tools": [{"url_context": {}}],
            },
        )
    return response.text
    
   # --- : CONVERT SUMMARY TO STRUCTURED JSON (NO TOOLS) ---
def convert_summary_to_json(summary: str, schema: dict) -> dict:
    """
    Take a natural-language summary and convert it into structured JSON
    using JSON Schema-based structured output. NO tools here.
    """
    prompt = (
        # YOUR CODE HERE : Prompt the AI to recieve a summary and extract fields such as : title, summary, and key takeaways.
        f'Convert the following text {summary} and fill the schema {schema} by extracting all fields such as : title, summary, and key takeaways.'
    )

    response = client.models.generate_content(
        model= "gemini-3-flash-preview" ,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": schema,
        },
    )

    # Thanks to structured output, this should be valid JSON text
    return json.loads(response.text)

# --- : ORCHESTRATOR: ARTICLE URL -> JSON OBJECT ---
def process_article_to_json(article_url: str, schema: dict) -> dict:
    """
    Full pipeline:
    1) Use URL Context to read and summarize the article.
    2) Convert that summary into structured JSON using the schema.
    """
    try:
        summary = fetch_article_summary(article_url)
    except Exception as e:
        return {"error": f"Error during URL Context summarization: {e}"}

    # Optionally, you can print or log the 'before' text here for the demo
    print("\n--- Raw Summary from URL Context (BEFORE) ---")
    print(summary)
    print("--------------------------------------------\n")

    try:
        structured = convert_summary_to_json(summary, schema)
        return structured
    except Exception as e:
        # If structured output fails, at least return the summary for inspection
        return {
            "error": f"Error during structured output: {e}",
            "raw_summary": summary,
        }


# --- EXECUTION ---
if __name__ == "__main__":
    TEST_URL = (
        article_url
    )

    result_data = process_article_to_json(TEST_URL, ARTICLE_SCHEMA)

    print("\n--- Structured Article Data (AFTER) ---")
    print(json.dumps(result_data, indent=2))
    print("---------------------------------------\n")