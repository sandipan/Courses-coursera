from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, ThinkingConfig

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env in your project folder

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


def get_coaching(prompt: str, style: str = "quick") -> None:
    """
    Generates a response from the AI coach, selecting model and (optionally)
    enabling thinking based on the requested style.

    style:
      - "quick":  gemini-3-flash-preview (fast, cost-efficient; thinking off)
      - "deep":   gemini-3-pro-preview   (deeper reasoning; thinking on)
    """
    print(f"\n--- INITIATING REQUEST: {style.upper()} COACHING ---")

    if style == "quick":
        model_name = "gemini-3-flash-preview"
        config = None  # thinking off by default
    elif style == "deep":
        model_name = "gemini-3.1-pro-preview"
        # Thinking controls live under thinking_config
        config = GenerateContentConfig(
            thinking_config=ThinkingConfig(
                thinking_level="high"
            )
        )
    else:
        raise ValueError("Invalid style. Use 'quick' or 'deep'.")

    print(f"MODEL SELECTED: {model_name}")

    try:
        resp = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config,
        )

        # Gemini 3 / google-genai: don't rely on "thought" parts being present.
        # If you requested thinking, you may still just get final text in resp.text.
        try:
            candidates = getattr(resp, "candidates", []) or []
            content = getattr(candidates[0], "content", None) if candidates else None
            parts = getattr(content, "parts", []) if content else []

            printed_header = False
            for part in parts:
                # Some SDK versions may expose "thought" parts; others won't.
                if getattr(part, "thought", False) and getattr(part, "text", ""):
                    if not printed_header:
                        print("\n🤔 MODEL'S THOUGHT SUMMARY:")
                        printed_header = True
                    print(part.text)

            if printed_header:
                print("-" * 20)
        except Exception:
            # Silently continue if structure differs or thoughts absent
            pass

        print("\n✅ FINAL RESPONSE:")
        print(getattr(resp, "text", ""))

    except Exception as e:
        print(f"\nAn error occurred: {e}. Check your API key, network, or SDK version.")

    print("-" * 30)


# --- Test calls ---
if __name__ == "__main__":
    print("Running tests...")
    get_coaching("What are three tips for public speaking?", style="quick")
    get_coaching("Write a short, motivational speech about overcoming challenges.", style="deep")