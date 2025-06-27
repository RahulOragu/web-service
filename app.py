from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Colab

# In-memory storage for latest chatbot response
latest_response = {"inference": "", "reason": "", "suggestions": ""}

@app.route("/", methods=["GET"])
def index():
    return "🚀 Flask server for Botpress Webhook is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        payload_text = data.get("payload", {}).get("text", "")

        # Extract fields using simple keyword markers (your bot must format like this)
        inference = reason = suggestions = ""
        if "Inference:" in payload_text:
            inference = payload_text.split("Inference:")[1].split("Reason:")[0].strip()
        if "Reason:" in payload_text:
            reason = payload_text.split("Reason:")[1].split("Suggestions:")[0].strip()
        if "Suggestions:" in payload_text:
            suggestions = payload_text.split("Suggestions:")[1].strip()

        latest_response.update({
            "inference": inference,
            "reason": reason,
            "suggestions": suggestions
        })

        return jsonify({"status": "success", "received": payload_text}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/latest", methods=["GET"])
def get_latest_response():
    return jsonify(latest_response), 200
