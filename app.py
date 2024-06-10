import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve API key from environment variables
API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Flask app
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)