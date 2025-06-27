from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_response = {"inference": "", "reason": "", "suggestions": ""}

@app.route("/", methods=["GET"])
def home():
    return "✅ Flask Webhook is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        text = data.get("payload", {}).get("text", "")

        # Keyword extraction
        inference = reason = suggestions = ""
        if "Inference:" in text:
            inference = text.split("Inference:")[1].split("Reason:")[0].strip()
        if "Reason:" in text:
            reason = text.split("Reason:")[1].split("Suggestions:")[0].strip()
        if "Suggestions:" in text:
            suggestions = text.split("Suggestions:")[1].strip()

        latest_response.update({
            "inference": inference,
            "reason": reason,
            "suggestions": suggestions
        })

        return jsonify({"status": "success", "stored": latest_response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/latest", methods=["GET"])
def latest():
    return jsonify(latest_response), 200
