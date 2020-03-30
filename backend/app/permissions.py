from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from app.models import Patient

class IsPatient(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return isinstance(request.user, Patient)

class IsOwnPatient(permissions.BasePermission):
    """
    Permission to modify information only if the patient is themselves
    """
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'owner'):
            return False
        return request.user == obj.owner
