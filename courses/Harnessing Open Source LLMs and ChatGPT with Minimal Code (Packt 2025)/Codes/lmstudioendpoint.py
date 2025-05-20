# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
    model="mathstral-7B-v0.1-GGUF/mathstral-7B-v0.1-Q3_K_L.gguf", #"IlyaGusev/saiga_mistral_7b_gguf",  
    messages=[
        {"role": "system", "content": "You are an expert in geography."},
        {
            "role": "user",
            "content": "What is the capital of Itlay? Answer in one sentence.",
        },
    ],
    temperature=0.1,
)

print(completion.choices[0].message.content)
