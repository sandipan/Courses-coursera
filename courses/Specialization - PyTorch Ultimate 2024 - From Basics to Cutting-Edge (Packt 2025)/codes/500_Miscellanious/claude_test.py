import anthropic

# ClUADE API KEY
# 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

client = anthropic.Anthropic(api_key='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')

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    system="You are a world-class poet. Respond only with short poems.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Why is the ocean salty?"
                }
            ]
        }
    ]
)
print(message.content)