import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Replace this with your actual n8n Webhook URL from the 'Webhook - Receive Lead & Email' node
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/outreach-agent" )

def test_live_campaign():
    """
    Script to test the live connection between Python/Streamlit and n8n Workflow.
    Matches exact keys expected by n8n Validate Payload node:
    - recipient_email
    - subject
    - email_body
    - recipient_name
    - recipient_company
    - recipient_phone
    """
    print("=" * 60)
    print("🚀 TESTING STREAMLIT/PYTHON TO n8n WORKFLOW CONNECTION")
    print("=" * 60)

    # Lead Data matching n8n Validate Payload IF node exactly
    test_payload = {
        "recipient_email": "faizadiba2004@gmail.com",
        "subject": "Exclusive AI Automation Strategy for AI Outreach Automation",
        "email_body": "Hi Adeeba,\n\nI noticed AI Outreach Automation has been expanding in the AI space. We help teams automate workflow processes, saving up to 15 hours weekly.\n\nWould you be open to a 10-minute discovery chat?\n\nBest regards,\nAdeeba Faiz",
        "recipient_name": "Adeeba Faiz",
        "recipient_company": "AI Outreach Automation",
        "recipient_phone": "+923494638576"
    }

    print(f"📡 Sending Lead Payload to n8n Webhook:")
    print(json.dumps(test_payload, indent=2))
    print("-" * 60)

    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code in (200, 201):
            print("✅ SUCCESS! n8n Webhook received the lead successfully!")
            print(f"n8n Response: {response.text}")
            print("\n🎉 Check your n8n canvas execution history—Validate Payload will now pass TRUE!")
        else:
            print(f"❌ FAILED with Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("Tip: Make sure n8n workflow is ACTIVE and webhook URL is correct.")

if __name__ == "__main__":
    test_live_campaign()
