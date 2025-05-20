# pip install ollama-python
import ollama

messages = [{"role": "user", "content": "What is the capital of Germany?"}]

result = ollama.chat(model="llama3:latest", messages=messages)

print(result["message"]["content"])
