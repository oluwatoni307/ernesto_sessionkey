from flask import Flask, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv  # using our internal organization's configuration module if available



app = Flask(__name__)
CORS(app)# Load environment variables from a .env file automatically
load_dotenv()

# Retrieve the API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")




if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

@app.route("/session", methods=["GET"])
def session():
    try:
        # Make a POST request to the OpenAI Real-Time Sessions endpoint
        response = requests.post(
            "https://api.openai.com/v1/realtime/sessions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-realtime-preview-2024-12-17",
                "voice": "verse",
                  "instructions": "you are a student and you want to ask me philosopical questions about life."
            },
        )

        # Check if the request was successful
        if response.status_code != 200:
            return jsonify({"error": "Failed to create session", "status_code": response.status_code}), response.status_code

        # Parse the JSON response from OpenAI
        data = response.json()
        print(data)

        # Send back the JSON we received from the OpenAI REST API
        return jsonify(data["client_secret"]["value"]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/wakeup", methods=["GET"])
def wakeup():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=3000)