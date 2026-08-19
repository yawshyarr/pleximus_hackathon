import logging
import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import chat

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat_route():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"error": "Request must include a 'message' field"}), 400
    message = data["message"]
    try:
        result = chat(message)
    except Exception:
        logging.exception("Unhandled error in /chat")
        return jsonify({"error": "Internal server error"}), 500
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5003)
