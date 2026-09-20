import os
import sys
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def check_everything():
    print("=" * 60)
    print("🩺 AI OUTREACH SYSTEM DIAGNOSTIC CHECKER")
    print("=" * 60)

    # 1. Check .env variables
    sender_email = os.getenv("SENDER_EMAIL", "").strip()
    app_password = os.getenv("APP_PASSWORD", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    bland_key = os.getenv("BLAND_API_KEY", "").strip()
    n8n_url = os.getenv("N8N_WEBHOOK_URL", "").strip()

    print(f"1. SENDER_EMAIL:   {'✅ SET (' + sender_email + ')' if sender_email else '❌ MISSING!'}")
    print(f"2. APP_PASSWORD:   {'✅ SET (' + str(len(app_password)) + ' chars)' if app_password else '❌ MISSING!'}")
    print(f"3. GEMINI_API_KEY: {'✅ SET' if gemini_key else '❌ MISSING!'}")
    print(f"4. BLAND_API_KEY:  {'✅ SET' if bland_key else '❌ MISSING! (Required for real calls)'}")
    print(f"5. N8N_WEBHOOK_URL:{'✅ SET (' + n8n_url + ')' if n8n_url else '❌ MISSING!'}")
    print("-" * 60)

    # 2. Test Direct Gmail SMTP Email
    print("\n📩 TESTING DIRECT EMAIL SENDING (Gmail SMTP)...")
    if sender_email and app_password:
        try:
            msg = MIMEText("Hi Adeeba! This is a test email from your AI Outreach Agent system.")
            msg['Subject'] = "🎉 Test Email - AI Outreach Agent"
            msg['From'] = sender_email
            msg['To'] = "faizadiba2004@gmail.com"

            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)

            print("✅ SUCCESS! Direct email sent to faizadiba2004@gmail.com. Check your inbox!")
        except Exception as e:
            print(f"❌ DIRECT EMAIL FAILED: {e}")
            print("Tip: Check if APP_PASSWORD is a 16-character Gmail App Password (not your normal password).")
    else:
        print("❌ SKIPPED Direct Email Test (SENDER_EMAIL or APP_PASSWORD missing in .env)")

    # 3. Test Direct Bland AI Call
    print("\n📞 TESTING DIRECT AI VOICE CALL (Bland AI API)...")
    if bland_key:
        try:
            url = "https://api.bland.ai/v1/calls"
            headers = {
                "authorization": bland_key,
                "Content-Type": "application/json"
            }
            payload = {
                "phone_number": "+923494638576",
                "task": "Call Adeeba regarding AI Outreach Automation follow-up.",
                "voice": "nat",
                "first_sentence": "Hi Adeeba, this is Alex testing the AI Outreach calling system!"
            }
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            res_json = response.json()
            print(f"Bland Response Code: {response.status_code}")
            print(f"Bland Response Data: {res_json}")

            if response.status_code == 200 and res_json.get("status") == "success":
                print("✅ SUCCESS! AI Voice Call dispatched! Your phone (+923494638576) should ring in 10 seconds!")
            else:
                print(f"❌ BLAND CALL FAILED: {res_json.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ BLAND CALL ERROR: {e}")
    else:
        print("❌ SKIPPED Bland Call Test (BLAND_API_KEY missing in .env)")

if __name__ == "__main__":
    check_everything()
