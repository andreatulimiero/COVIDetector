from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import SimpleRouter

from app import views

router = SimpleRouter()
router.register(r'register', views.RegisterViewSet)
router.register(r'samples', views.SampleViewSet)
router.register(r'patients', views.PatientViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
