import os
from celery import shared_task
from twilio.rest import Client

@shared_task
def send_sms_reminder_task(username, message):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_FROM_NUMBER')
    to_number = os.environ.get('TEST_PHONE_NUMBER')  

    if not all([account_sid, auth_token, from_number, to_number]):
        print("Twilio configuration incomplete.")
        return

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Hello {username}! {message}",
        from_=from_number,
        to=to_number
    )
