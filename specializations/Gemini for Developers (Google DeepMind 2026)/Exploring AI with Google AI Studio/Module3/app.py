# pip install -U google-genai python-dotenv
# pip install google-generativeai

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env located next to this script
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    try:
        # This is the original line from your exported code
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        model = "gemini-3-flash-preview"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="Create a 3 day itinerary for a trip to Japan."),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level="HIGH",
            ),
        )

        # Process the successful response here
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            print(chunk.text, end="")

    except Exception as e:
        # This block runs ONLY if the API call or connection fails
        print(f"An error occurred: {e}")
        print("Connection error. Please check your network or API key.")

if __name__ == "__main__":
    generate()