import os
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.models import Sample
from app.tasks import upload_sample, analyze_sample

def send_registration_email(email: str, token: str):
    if settings.DEBUG:
        print('Not sending email in DEBUG mode, token:{}'.format(token))
        return
    message = Mail(
            from_email='info@andreatulimiero.com',
            to_emails=email,
            subject='User registration confirmation',
            html_content='Thanks for registering!<br/>Please finish your account setup by going <a href="http://localhost:8080/#/confirm?token={}">here</a>'.format(token))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e.message)


def upload_and_analyze_sample(sample: Sample, audio: str):
    # Upload the sample to S3
    upload_sample.delay(sample.id, audio)
    # Carry out prediction locally
    analyze_sample.delay(sample.id, audio)
