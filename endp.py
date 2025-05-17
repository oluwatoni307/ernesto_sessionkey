from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

@app.route("/session", methods=["POST"])
def session():
    try:
        # Extract JSON body from request
        data = request.get_json()
        selected_voice = data.get("voice", "nova")  # fallback to 'nova' if none provided

        # Make a POST request to the OpenAI Real-Time Sessions endpoint
        response = requests.post(
            "https://api.openai.com/v1/realtime/sessions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-realtime-preview-2024-12-17",
                "voice": selected_voice,
                "instructions": "you are a student and you want to ask me philosophical questions about life."
            },
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to create session", "status_code": response.status_code}), response.status_code

        return jsonify(response.json().get("client_secret", {}).get("value", {})), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/wakeup", methods=["GET"])
def wakeup():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=3000)
