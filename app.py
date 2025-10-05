from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if not data or "message" not in data:
        return "no message", 200

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "").strip()

    if text.startswith("/start"):
        send_message(chat_id, "👋 Hello! Send me a phone number to get info.")
    else:
        number = "".join(ch for ch in text if ch.isdigit())
        if not number:
            send_message(chat_id, "Please send a valid phone number or /start")
        else:
            info = f"📱 Number: {number}\n🌍 Country: India (demo info)"
            send_message(chat_id, info)
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot running successfully!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))