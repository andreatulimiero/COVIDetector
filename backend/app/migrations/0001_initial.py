# Generated by Django 3.0.4 on 2020-03-30 14:38

import app.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.CharField(default=app.models.gen_patient_token, max_length=64, primary_key=True, serialize=False)),
                ('secret', models.CharField(default=app.models.gen_patient_token, max_length=64)),
                ('age_range', models.CharField(choices=[('1', '0-9'), ('2', '10-19'), ('3', '20-29'), ('4', '30-39'), ('5', '40-49'), ('6', '50-59'), ('7', '60-69'), ('8', '70-79'), ('9', '80-89'), ('10', '90-99'), ('11', '100+')], max_length=2, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('email', models.EmailField(max_length=256, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded', models.BooleanField(default=False)),
                ('analyzed', models.BooleanField(default=False)),
                ('sick', models.BooleanField(default=False)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='app.Patient')),
            ],
        ),
    ]
