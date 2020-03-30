from __future__ import absolute_import, unicode_literals
import os
import time
import tempfile

import boto3
from celery import subtask, shared_task

from app.models import Sample

@shared_task
def upload_sample(sample_id: str, audio: str):
    print('Creating temp file ...')
    f = tempfile.NamedTemporaryFile()
    f.write(audio.encode())
    f.flush()
    del(audio)
    print('Uploading file ...')
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    s3.upload_file(f.name, 'covidetector', 'samples/{}'.format(sample_id))
    time.sleep(10)
    f.close()
    subtask(upload_sample_cb).delay(sample_id)

@shared_task
def upload_sample_cb(sample_id: str):
        print('Upload complete: {}'.format(sample_id))
        sample = Sample.objects.get(id=sample_id)
        sample.uploaded = True
        sample.save()

@shared_task
def analyze_sample(sample_id: str, audio: str):
    subtask(analyze_sample_cb).delay(sample_id)

@shared_task
def analyze_sample_cb(sample_id: str):
        print('Analysis complete: ', sample_id)
        sample = Sample.objects.get(id=sample_id)
