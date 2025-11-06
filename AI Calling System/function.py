import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT = os.getenv("TWILIO_ACCOUNT_SID")
TOKEN   = os.getenv("TWILIO_AUTH_TOKEN")
FROM    = os.getenv("TWILIO_NUMBER")

client = Client(ACCOUNT, TOKEN)
to = input("Enter number to call (10 or +91...): ").strip()
if not to.startswith("+"):
    to = "+91" + to   # optional India format

call = client.calls.create(
    to=to,
    from_=FROM,
    twiml="<Response><Say voice='alice'>Hello! This is a test call from your Autodialer app.</Say></Response>"
)

print("\n✅ CALL INITIATED\nCall SID:", call.sid)
