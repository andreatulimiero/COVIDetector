from django.contrib import admin

from app.models import (
        Registration,
        Patient,
        Sample)

admin.site.register(Registration)
admin.site.register(Patient)
admin.site.register(Sample)
