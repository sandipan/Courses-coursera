import json
import openai
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {
        "role": "system",
        "content": "You are a stockbroker who returns current stock prices",
    }
]


def getprice(ticker):
    tk = yf.Ticker(ticker)
    return json.dumps(tk.info.get("currentPrice"))


# result = getprice("MSFT")
# print(result)
func = [
    {
        "name": "getprice",
        "description": "Returns the current price for the given stock ticker",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The name of the stock which we want the current price for",
                }
            },
            "required": ["ticker"],
        },
    }
]

client = openai.Client()


def start(message):
    m = {"role": "user", "content": message}
    messages.append(m)
    result = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", messages=messages, functions=func
    )
    return result.choices[0].message


question = "What is the current stock price of TESLA"
question = "What is the current stock price of Microsoft"
modelanswer = start(question)

print(modelanswer)

arguments = json.loads(modelanswer.function_call.arguments).get("ticker")
functionname = modelanswer.function_call.name

final_result = eval(functionname)(arguments)
print(final_result)
