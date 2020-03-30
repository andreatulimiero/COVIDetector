from rest_framework import authentication
from rest_framework import exceptions

from app.models import Patient

class AnonAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Hackish enough, we use patient instead of the canonical User object :D
        token = request.META.get('HTTP_X_PATIENT_TOKEN')
        secret = request.META.get('HTTP_X_PATIENT_SECRET')
        if not token or not secret:
            return None
        try:
            patient = Patient.objects.get(id=token, secret=secret)
        except Patient.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such patient')
        return (patient, None)
