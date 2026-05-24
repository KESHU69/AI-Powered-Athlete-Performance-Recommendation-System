from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import time
import os

app = Flask(__name__)
# Allows your HTML/JS frontend to communicate with this Python server
CORS(app) 

# --- CONFIGURATION ---
# Replace these with your actual keys from the OpenAI Dashboard
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Initialize the OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_message = user_data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # 1. Create a new conversation thread for the athlete
        thread = client.beta.threads.create()

        # 2. Add the athlete's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        # 3. Run the Assistant (This triggers the Vector Search / RAG)
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # 4. Wait for the Assistant to finish searching and generating
        while run.status in ['queued', 'in_progress']:
            time.sleep(1) # Check status every 1 second
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # 5. Retrieve and format the response for the frontend
# 5. Retrieve and format the response for the frontend
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            # The most recent message is the bot's reply
            bot_reply = messages.data[0].content[0].text.value
            return jsonify({"reply": bot_reply})
            
        elif run.status == 'failed':
            # This will catch exactly why OpenAI rejected the request
            error_msg = run.last_error.message if run.last_error else "Unknown error"
            print(f"OPENAI ERROR: {error_msg}")
            return jsonify({"reply": f"OpenAI Error: {error_msg}"}), 500
            
        else:
            return jsonify({"reply": f"Sorry, run ended with status: {run.status}"}), 500

    except Exception as e:
        return jsonify({"reply": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Athlete Coach Server on port 5000...")
    app.run(port=5000, debug=True)