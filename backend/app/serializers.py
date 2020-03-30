from rest_framework import serializers
from app.models import Registration, Patient, Sample

from app.utils import upload_and_analyze_sample, send_registration_email

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('email',)

    def create(self, validated_data) -> Registration:
        reg = super().create(validated_data)
        send_registration_email(reg.email, reg.token)
        return reg

class PatientSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Patient
        exclude = ('secret',)

class SampleSerializer(serializers.ModelSerializer):
    audio = serializers.CharField(write_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Sample
        fields = ('id', 'patient', 'created_at', 'audio', 'url', 'sick')

    def create(self, validated_data):
        audio = validated_data.pop('audio')
        sample = super().create(validated_data)
        upload_and_analyze_sample(sample, audio)
        return sample

    def get_url(self, sample):
        _URL = 'https://covidetector.s3.eu-central-1.amazonaws.com/samples/{}'
        return _URL.format(sample.id)

class ResultSerializer(serializers.ModelSerializer):
    pass
