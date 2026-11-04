import os
from google import genai
from dotenv import load_dotenv
from google.genai import types       
        
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
        
        '''
        # Task 1
        prompt = "Act as a literary poet. Write a long poem (at least 40 lines) about time and life. Use vivid imagery, a reflective tone, and a repeating motif (like a clock, ocean tide, or seasons). Include 5–7 stanzas with a strong ending that feels hopeful but honest."
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        # Print the response
        print("\n--- AI Response ---")
        print(response.text)
        print("-------------------")
        '''

        '''
        # Task 2
        prompt = 'Generate a high-resolution landscape image of a wide valley covered in colorful wildflowers, with scattered oak and pine trees, golden-hour sunlight, soft mist in the distance, and mountains on the horizon. Cinematic composition, ultra-detailed, natural colors, 16:9 aspect ratio.'
        #prompt =  "An umbrella in the foreground, and a rainy night sky "
        #        "in the background. Cinematic lighting, realistic details."
        # Generate the image using Gemini API
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-image', #"gemini-2.5-flash-image"
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="9:16",
                ),
            ),
        )
        for part in response.parts:
            if part.inline_data:
                generated_image = part.as_image()
                generated_image.show()
        '''

        '''
        # Task 3
        prompt = "Write a story in exactly 3 paragraphs about a brave explorer who discovers something unexpected. Keep it vivid and emotional, with a clear beginning, conflict, and resolution. Aim for an adventurous tone and end with a memorable final sentence."
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        # Print the response
        print("\n--- AI Response ---")
        print(response.text)
        print("-------------------")
        '''

        # Task 4
        prompt = 'Create a detailed jungle scene in daylight with lush green foliage, sun rays filtering through the canopy, and a variety of animals visible: a toucan on a branch, a monkey in the midground, a jaguar partially hidden in tall plants, colorful frogs near a stream, and butterflies in the foreground. High detail, realistic style, balanced composition, 16:9 aspect ratio.'
        # Generate the image using Gemini API
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-image', #"gemini-2.5-flash-image"
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="9:16",
                ),
            ),
        )
        for part in response.parts:
            if part.inline_data:
                generated_image = part.as_image()
                generated_image.save("jungle.png")
                generated_image.show()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()