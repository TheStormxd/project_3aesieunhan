import os
from flask import Flask, request, jsonify, redirect, url_for, make_response
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS


import mysql.connector
import warnings
warnings.filterwarnings('ignore')

mysql_host = "localhost"
mysql_user = "kienle"
mysql_password = "kienle201"
mysql_database = "tutor_chatbot"

cursor = None


API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# Function to configure the Generative AI model
def configure_model(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        print(f"Error configuring model: {e}")
        return None

# Function to start a chat session
def start_chat(model):
    try:
        chat = model.start_chat(history=[])
        return chat
    except Exception as e:
        print(f"Error starting chat: {e}")
        return None

model = configure_model(API_KEY)
chat = start_chat(model)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    if not chat:
        return jsonify({'error': 'Chat session not initialized'}), 500

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    instruction = "Act like you are a chatbot tutor that help the student in HCI course"
    try:
        response = chat.send_message(instruction + user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"Error during chat interaction: {e}")
        return jsonify({'error': 'Failed to get response from AI'}), 500

@app.route('/api/admin', methods=['GET'])
def get_user():
    # Establish a connection to the database
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        port=3306
    )

    cursor = connection.cursor()

    query = 'SELECT * FROM users'
    cursor.execute(query)
    result = cursor.fetchall()
    return jsonify(result), 200

@app.route('/api/signup', methods=['POST'])
def create_user():
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        port=3306
    )
    cursor = connection.cursor()
    username = request.args.get("username")
    print(username)
    password = request.args.get("password")
    print(password)
    query = "INSERT INTO Users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    connection.commit()
    return jsonify({'Success': 'sign up successssss'}), 200

@app.route('/api/signin', methods=['POST'])
def login():
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        port=3306
    )
    cursor = connection.cursor()
    username = request.args.get("username")
    print(username)
    password = request.args.get("password")
    print(password)
    query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
    cursor.execute(query, (username, password))      
    result = cursor.fetchall() 

    if (len(result) == 0):
        print("Error")
        # return jsonify({'error': 'Sign Up Failed'}, status=200)
        return make_response(jsonify({"error": 'error'}), 404)
    else:
        print("Success")
        return make_response(jsonify({"success": 'success'}), 200)

if __name__ == '__main__':
    app.run(debug=True, port=5000)