from django.shortcuts import render, get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.status import (
        HTTP_200_OK,
        HTTP_204_NO_CONTENT,
        HTTP_429_TOO_MANY_REQUESTS)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, action

from app.serializers import (
        RegistrationSerializer,
        PatientSerializer,
        SampleSerializer)
from app.permissions import IsPatient, IsOwnPatient
from app.models import Registration, Patient, Sample
from app.utils import send_registration_email

class RegisterViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    @action(methods=['post'], detail=False)
    def confirm(self, req):
        reg = get_object_or_404(Registration, token=req.data['token'])
        if reg.confirmed:
            err = {"err":"Token already requested"}
            return Response(err, status=HTTP_429_TOO_MANY_REQUESTS)
        patient = Patient.objects.create()
        res = {"token": patient.id, "secret": patient.secret}
        reg.confirmed = True
        reg.save()
        return Response(res, status=HTTP_200_OK)

class PatientViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsPatient, IsOwnPatient]
    renderer_classes = [JSONRenderer]

class SampleViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsPatient]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        if self.request.method == 'GET':
            self.queryset = self.queryset.filter(uploaded=True)
        return self.queryset

    def create(self, req):
        sample_ser = self.get_serializer(data=req.data)
        sample_ser.is_valid(raise_exception=True)
        patient = sample_ser.validated_data['patient']
        (err, msg, status) = patient.can_send_sample()
        if err:
            return Response(msg)
        sample_ser.save()
        return Response(status=HTTP_204_NO_CONTENT)
