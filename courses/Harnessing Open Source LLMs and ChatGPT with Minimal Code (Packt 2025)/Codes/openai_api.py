import openai
import os
#pip install -U python-dotenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")
#print(openai.api_key)

client = openai.Client()

messages = [
    {"role": "user", "content": "List 3 reasons why strength training is healthy"}
]

result = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)

print(result)
print("------------------------------")
print(result.choices[0].message.content)
