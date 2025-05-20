import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.Client()

messages = [
    {"role": "user", "content": "List 3 reasons why cardio training is healthy?"}
]

result = client.chat.completions.create(
    model="gpt-3.5-turbo-1106", messages=messages, stream=True
)

for chunk in result:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
