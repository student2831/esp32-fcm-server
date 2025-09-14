import os
import json
import requests
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from google.auth.transport.requests import Request

app = Flask(__name__)

# کلید سرویس را از Environment Variable به‌صورت رشتهٔ JSON می‌گیریم
# (در پنل Render باید Environment Variable با نام SERVICE_ACCOUNT_JSON ست شود)
service_account_info = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])

# ساخت credentials برای دسترسی به Firebase Cloud Messaging v1
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/firebase.messaging"]
)

@app.route("/send", methods=["POST"])
def send():
    """
    انتظار یک JSON با فیلدهای زیر:
    {
      "token": "<device_fcm_token>",
      "title": "اختیاری - عنوان نوتیفیکیشن",
      "body":  "اختیاری - متن نوتیفیکیشن"
    }
    """

    # گرفتن یک access token تازه از Google
    credentials.refresh(Request())
    access_token = credentials.token

    data = request.get_json(force=True)
    token = data.get("token")
    title = data.get("title", "Alert")
    body  = data.get("body", "Message from ESP32")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    # ارسال درخواست به Firebase Cloud Messaging
    r = requests.post(
        f"https://fcm.googleapis.com/v1/projects/{service_account_info['project_id']}/messages:send",
        headers=headers,
        json=payload
    )

    return jsonify(r.json()), r.status_code


if __name__ == "__main__":
    # اجرای Flask روی پورت 8080 برای سرویس‌دهی در Render
    app.run(host="0.0.0.0", port=8080)
