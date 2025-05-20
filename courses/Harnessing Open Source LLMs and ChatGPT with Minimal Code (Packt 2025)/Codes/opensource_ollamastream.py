import ollama

while True:

    question = input("Ask your question ")

    messages = [
        {
            "role": "user",
            "content": question,
        }
    ]

    result = ollama.chat(model="llama3:latest", messages=messages, stream=True)

    for chunk in result:
        print(chunk["message"]["content"], end="", flush=True)
