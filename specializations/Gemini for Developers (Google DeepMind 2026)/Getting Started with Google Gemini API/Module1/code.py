import os
from google import genai
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        print("Please create a .env file and add your API key.")
        return

    try:
        # Create the client (google-genai SDK)
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="Write a short poem about the moon."
        )

        # Print the response
        print("\n--- AI Response ---")
        print(response.text)
        print("-------------------")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()