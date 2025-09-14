from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
FCM_KEY = os.environ.get("FCM_KEY")   # توکن سرور فایربیس رو تو Render به صورت Environment Variable ست می‌کنی

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    token = data.get("token")
    title = data.get("title", "Alert")
    body  = data.get("body", "Message from ESP32")

    r = requests.post(
        "https://fcm.googleapis.com/fcm/send",
        headers={"Authorization": f"key={FCM_KEY}", "Content-Type": "application/json"},
        json={"to": token, "notification": {"title": title, "body": body}}
    )
    return jsonify(r.json())
