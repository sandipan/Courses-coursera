import os
import json
from dotenv import load_dotenv
from google import genai

# Load variables from .env into the environment
load_dotenv()

# ---  JSON SCHEMA FOR STRUCTURED OUTPUT ---
ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "key_takeaways": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3,
        },
    },
    "required": ["title", "summary", "key_takeaways"],
}

# ---  CREATE CLIENT (new google-genai style) ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("FATAL ERROR: GEMINI_API_KEY environment variable not set.")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

# The URL of the article to analyze
article_url = "https://developers.googleblog.com/gemini-3-flash-is-now-available-in-gemini-cli/"


# ---  FETCH ARTICLE SUMMARY USING URL CONTEXT (TOOLS) ---
def fetch_article_summary(article_url: str) -> str:
    """
    Use URL Context to read the article and return a concise summary.
    This call uses tools, so we DO NOT request JSON here.
    """
    prompt = (
        "You are an article analysis assistant.\n"
        "Use URL Context to read the article at the URL below.\n"
        "Return a concise paragraph summarizing the article and mention its title.\n\n"
        f"URL: {article_url}\n"
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
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
        "You will receive an article summary.\n"
        "Extract the following fields and respond ONLY with JSON:\n"
        "- title: the article title\n"
        "- summary: a short paragraph summary\n"
        "- key_takeaways: exactly three bullet-style strings\n\n"
        "Article summary:\n"
        f"{summary}\n"
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": schema,
        },
    )

    # Thanks to structured output, this should be valid JSON text
    return json.loads(response.text)


# ---  ORCHESTRATOR: ARTICLE URL -> JSON OBJECT ---
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