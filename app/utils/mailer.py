# import os
# import requests

# BREVO_API_KEY = os.getenv("BREVO_API_KEY")
# TO_EMAIL = os.getenv("SCIQUS_NOTIFY_EMAIL")
# FROM_EMAIL = os.getenv("FROM_EMAIL")

# def notify_sciqus_owner(company: str, question: str):
#     if not BREVO_API_KEY:
#         print("⚠️ BREVO_API_KEY not configured")
#         return

#     url = "https://api.brevo.com/v3/smtp/email"

#     headers = {
#         "accept": "application/json",
#         "api-key": BREVO_API_KEY,
#         "content-type": "application/json"
#     }

#     payload = {
#         "sender": {
#             "email": FROM_EMAIL,
#             "name": "Sciqus Lead Bot"
#         },
#         "to": [
#             {"email": TO_EMAIL}
#         ],
#         "subject": "🚀 New Business Lead from Sciqus Website",
#         "htmlContent": f"""
#         <h2>New Lead Captured</h2>
#         <p><b>Company / User:</b> {company}</p>
#         <p><b>Question:</b></p>
#         <p>{question}</p>
#         <br/>
#         <p>— Sciqus AMS Chatbot</p>
#         """
#     }

#     # response = requests.post(url, headers=headers, json=payload)

#     # if response.status_code not in [200, 201, 202]:
#     #     raise Exception(f"Brevo error: {response.status_code} {response.text}")

#     # print("✅ Lead email sent successfully")
#     response = requests.post(url, headers=headers, json=payload)

#     print("📧 Brevo status:", response.status_code)
#     print("📧 Brevo response:", response.text)

#     if response.status_code not in [200, 201, 202]:
#         raise Exception(f"Brevo error: {response.status_code} {response.text}")
import os
import requests

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
TO_EMAIL = os.getenv("SCIQUS_NOTIFY_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def notify_sciqus_owner(company: str, question: str):
    if not BREVO_API_KEY or not TO_EMAIL or not FROM_EMAIL:
        print("⚠️ Email config missing")
        return

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "email": FROM_EMAIL,
            "name": "Sciqus Lead Bot"
        },
        "to": [{"email": TO_EMAIL}],
        "subject": "🚀 New Business Lead from Sciqus Website",
        "htmlContent": f"""
        <h2>New Lead Captured</h2>
        <p><b>Company / User:</b> {company}</p>
        <p><b>Question:</b></p>
        <p>{question}</p>
        <br/>
        <p>— Sciqus AMS Chatbot</p>
        """
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=3  # ✅ HARD TIMEOUT
        )

        print("📧 Brevo status:", response.status_code)

    except Exception as e:
        # ❌ NEVER raise
        print("❌ Email send failed:", e)