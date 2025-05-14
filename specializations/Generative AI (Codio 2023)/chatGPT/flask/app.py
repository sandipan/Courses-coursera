from flask import Flask, jsonify, request, render_template
import os 

# initialization
app = Flask(__name__)

# Route for handling session search
@app.route('/get_name', methods=["POST"])
def get_name():
	session_dict = {'coder', 'dev', 'test'}
	user_name = request.json["user_name"]  # Get the user input from the request
	print(f"checking if {user_name} is in session...")
	exists = f"{user_name} exists in session" if user_name in session_dict else f"{user_name} does not exist in session"
	output = {"name": exists}
	return jsonify(output)
	
# Routes for the home page
@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")  # Render the index.html template
	
if __name__ == '__main__':
    app.run(debug=True)