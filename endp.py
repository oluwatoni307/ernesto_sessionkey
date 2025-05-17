from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)

# Allow all origins (you can restrict this to your frontend URL in production)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load environment variables
load_dotenv()

# Get OpenAI API Key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

@app.route("/session", methods=["POST"])
def session():
    try:
        # Debug logging to inspect incoming requests
        print("---- /session endpoint hit ----")
        print("Headers:", dict(request.headers))
        print("Raw body:", request.data.decode())
        data = request.get_json(force=True, silent=True)
        print("Parsed JSON:", data)

        if not data:
            return jsonify({"error": "Missing or invalid JSON body"}), 400

        selected_voice = data.get("voice", "nova")

        # Send request to OpenAI to create a real-time session
        response = requests.post(
            "https://api.openai.com/v1/realtime/sessions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-realtime-preview-2024-12-17",
                "voice": selected_voice,
                "instructions": "You are a student and you want to ask me philosophical questions about life."
            },
        )

        if response.status_code != 200:
            print("OpenAI API error:", response.status_code, response.text)
            return jsonify({
                "error": "Failed to create session",
                "status_code": response.status_code,
                "details": response.text
            }), response.status_code

        session_data = response.json()
        print("OpenAI response:", session_data)

        return jsonify(response.json().get("client_secret", {}).get("value", {})), 200

    except Exception as e:
        print("Exception in /session:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/wakeup", methods=["GET"])
def wakeup():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=3000)
