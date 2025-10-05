from flask import Flask, request
import requests
import os
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")  # Replit Secrets me add karna

# Function to send message to Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if not data or "message" not in data:
        return "no message", 200

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "").strip()

    if text.startswith("/start"):
        send_message(chat_id, "👋 Hello! Send me a phone number (with country code) to get detailed info.")
    else:
        # Extract digits and plus sign
        number_text = "".join(ch for ch in text if ch.isdigit() or ch == '+')
        if not number_text.startswith("+"):
            send_message(chat_id, "❌ Please include country code, e.g., +911234567890")
            return "ok", 200

        try:
            parsed_number = phonenumbers.parse(number_text)
            
            country = geocoder.description_for_number(parsed_number, "en")
            carrier_name = carrier.name_for_number(parsed_number, "en")
            timezones_list = timezone.time_zones_for_number(parsed_number)
            number_type = phonenumbers.number_type(parsed_number)
            
            type_dict = {
                0: "FIXED_LINE",
                1: "MOBILE",
                2: "FIXED_LINE_OR_MOBILE",
                3: "TOLL_FREE",
                4: "PREMIUM_RATE",
                5: "SHARED_COST",
                6: "VOIP",
                7: "PERSONAL_NUMBER",
                8: "PAGER",
                9: "UAN",
                10: "VOICEMAIL",
                99: "UNKNOWN"
            }
            type_name = type_dict.get(number_type, "UNKNOWN")

            info = f"📱 Number: {number_text}\n" \
                   f"🌍 Country: {country}\n" \
                   f"📶 Carrier: {carrier_name}\n" \
                   f"⏰ Timezone(s): {', '.join(timezones_list)}\n" \
                   f"🔹 Type: {type_name}"

            send_message(chat_id, info)

        except Exception as e:
            send_message(chat_id, f"❌ Invalid number or error: {e}")

    return "ok", 200

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Bot running successfully!", 200

# Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
