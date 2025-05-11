import openai
from flask import Flask, jsonify, request, render_template
import os

# Set environment variables
#keys = os.getenv('OPENAI_KEY')  # Get the OpenAI API key from environment variable

#api_key = keys

openai.api_key='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'
app = Flask(__name__)

# Function to generate chatbot response
def generate_chat_response(user_input):
    prompt = user_input
    # Create a chat completion request using OpenAI's GPT-3.5 Turbo model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    # Extract the generated chat response from the API response
    chat_response = response['choices'][0]['message']['content'].strip()
    return chat_response

# Route for handling chat requests
@app.route("/chat", methods=["POST"])
def chat():
	user_input = request.json["user_input"]  # Get the user input from the request
	# Generate chatbot response using the user input
	print(user_input)
	chat_response = generate_chat_response(user_input)
	print(chat_response)
	response_data = {"ans": chat_response}
	return jsonify(response_data)
		
# Routes for the home page
@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")  # Render the index.html template

if __name__ == "__main__":
    #app.run(host='0.0.0.0')  # Run the Flask application on the host '0.0.0.0'
    app.run(debug=True)