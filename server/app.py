"""Kyurem — Unova Boundary Chatbot. Flask backend + Gemini 3.8 Flash brain."""
import os
import uuid
import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from utils.gemini_brain import KyuremBrain

# Load .env (GEMINI_API_KEY, GEMINI_MODEL, PORT)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent  # chatbot/
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR), static_folder=str(STATIC_DIR))
CORS(app)

brain = KyuremBrain()

# In-memory sessions: {session_id: [{role, content, time}]}
sessions: dict = {}


def get_session(session_id: str):
    if not session_id:
        session_id = f"kyurem_{uuid.uuid4().hex[:12]}"
    if session_id not in sessions:
        sessions[session_id] = []
    return session_id, sessions[session_id]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "app": "Kyurem",
        "region": "Unova",
        "dex": 646,
        "model": brain.model,
        "gemini_online": brain.online,
        "active_sessions": len(sessions),
        "timestamp": datetime.datetime.now().isoformat(),
    })


@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.get_json(force=True, silent=True) or {}
        user_text = (data.get("message") or "").strip()
        session_id = (data.get("session_id") or "").strip()

        if not user_text:
            return jsonify({"error": "Message is required"}), 400

        session_id, history = get_session(session_id)

        reply = brain.generate(history, user_text)
        now = datetime.datetime.now().isoformat()
        history.append({"role": "user", "content": user_text, "time": now})
        history.append({"role": "assistant", "content": reply, "time": now})

        # Cap history to last 60 messages
        if len(history) > 60:
            sessions[session_id] = history[-60:]

        return jsonify({
            "reply": reply,
            "session_id": session_id,
            "model": brain.model,
            "timestamp": now,
        })
    except Exception as e:
        print(f"[Kyurem] /api/chat error: {e}")
        return jsonify({"error": "Failed to process message", "details": str(e)}), 500


# Backward-compat alias for old client (POST /chat)
@app.route("/chat", methods=["POST"])
def chat_alias():
    return api_chat()


@app.route("/api/history/<session_id>", methods=["GET"])
def api_history(session_id):
    history = sessions.get(session_id, [])
    return jsonify({
        "session_id": session_id,
        "messages": history,
        "message_count": len(history),
    })


@app.route("/api/clear", methods=["POST"])
def api_clear():
    data = request.get_json(force=True, silent=True) or {}
    session_id = (data.get("session_id") or "").strip()
    if session_id in sessions:
        sessions[session_id] = []
    new_id = f"kyurem_{uuid.uuid4().hex[:12]}"
    sessions[new_id] = []
    return jsonify({"message": "Session cleared", "session_id": new_id})


@app.route("/api/model", methods=["GET"])
def api_model():
    return jsonify({"model": brain.model, "online": brain.online})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    print("❄ Kyurem awakening...")
    print(f"   Model : {brain.model} ({'online' if brain.online else 'offline — set GEMINI_API_KEY'})")
    print(f"   Serve : http://127.0.0.1:{port}")
    print("   Logo  : place your Kyurem image at static/kyurem.png")
    app.run(debug=True, host="127.0.0.1", port=port)
