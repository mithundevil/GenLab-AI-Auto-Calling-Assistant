import urllib.parse
from twilio.rest import Client
from config.settings import settings

class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def trigger_outbound_call(self, to_number: str, lead_name: str):
        try:
            # URL-encode the name to handle spaces/special characters
            encoded_name = urllib.parse.quote(lead_name)
            
            # The URL Twilio will hit to get TwiML instructions
            callback_url = f"{settings.BASE_URL}/api/ai-call?name={encoded_name}"
            
            call = self.client.calls.create(
                to=to_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                url=callback_url
            )
            print(f"Call triggered successfully: {call.sid}")
            return call.sid
        except Exception as e:
            print(f"Error triggering Twilio call: {e}")
            return None

twilio_service = TwilioService()
