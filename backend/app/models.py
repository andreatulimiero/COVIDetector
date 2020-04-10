import uuid
import secrets
from datetime import datetime, timedelta, timezone

from django.db import models

from rest_framework.status import HTTP_429_TOO_MANY_REQUESTS

SECURE_TOKEN_LENGTH = 32
SECRET_TOKEN_LENGTH = 32

#  SAMPLE_SUBMISSION_RATE = timedelta(hours=12)
SAMPLE_SUBMISSION_RATE = timedelta(hours=0)

class Registration(models.Model):
    email = models.EmailField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(
            primary_key = True,
            default = uuid.uuid4,
            editable = False)
    confirmed = models.BooleanField(default=False)

def gen_patient_token() -> str:
    """ Returns a secure anonymous random token """
    return secrets.token_hex(SECURE_TOKEN_LENGTH)

def gen_patient_secret() -> str:
    """ Returns a secure anonymous random token """
    return secrets.token_hex(SECRET_TOKEN_LENGTH)

class Patient(models.Model):
    id = models.CharField(primary_key=True, max_length=SECURE_TOKEN_LENGTH*2, default=gen_patient_token)
    secret = models.CharField(max_length=SECRET_TOKEN_LENGTH*2, default=gen_patient_token)
    AGE_RANGES = (
            ('1', '0-9'),
            ('2', '10-19'),
            ('3', '20-29'),
            ('4', '30-39'),
            ('5', '40-49'),
            ('6', '50-59'),
            ('7', '60-69'),
            ('8', '70-79'),
            ('9', '80-89'),
            ('10', '90-99'),
            ('11', '100+'),
            )
    age_range = models.CharField(max_length=2, choices=AGE_RANGES, null=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)

    def can_send_sample(self):
        last_sample = self.samples.order_by('-created_at').first()
        err, msg, status = False, None, None
        if last_sample:
            now = datetime.now(timezone.utc)
            diff = now - last_sample.created_at
            err = diff < SAMPLE_SUBMISSION_RATE
            msg = {'err': 'You should wait before submitting another sample'}
            status = HTTP_429_TOO_MANY_REQUESTS
        return (err, msg, status)

    @property
    def owner(self):
        return self

class Sample(models.Model):
    id = models.UUIDField(
            primary_key = True,
            default = uuid.uuid4,
            editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='samples')
    uploaded = models.BooleanField(default=False)
    analyzed = models.BooleanField(default=False)
    sick = models.BooleanField(default=False)
