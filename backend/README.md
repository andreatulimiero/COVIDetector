Backend
---
# Dependencies
Other than the requirements in `requirements.txt`,  `rabbitmq-server` is needed.
Debian based distro can install it with `sudo apt install rabbitmq-server` (should be easy for other distro as well).
# Start the backend
To start the backend run the following commands
```
python manage.py makemigrations
python manage.py migrate
celery -A covidetector worker -l info # Blocking
python manage.py runserver # Blocking
```

# Endpoints

### Legend
```
/blah/ -> Means that the endpoint returns something
/blah/ <- Means that these are the required input from the endpoint
?"blah" means a field is optional
{a, b, c} means a field can be only one of the following values
```
## Authentication
To carry out non-GET requests authentication is needed.
Authenticating a request is as adding the two tokens received at confirmation time in the request, namely:
- `X-PATIENT-TOKEN -> <patient_token>`
- `X-PATIENT-SECRET -> <patient_secret_token>`

## Registration
```
[POST] /api/register/ <- {"email":"<user_email>"}
[POST] /api/register/confirm/ <- {"token":"<confirmation_token>"} -> {"token":"<patient_token>", "secret":"<patient_secret_token>"}
```

## Samples
```
[POST] /api/samples/ <- {"patient":"<patient_token>", "audio":"<base64_audio>"} -> {}
[GET] /api/samples/ -> [{"id": "<sample_id>", "patient":"<patient_token>", "created_at":"timestamp"}
```

## Patients
```
[PUT] /api/patients/<patient_token>/ <- {?"age_range": "{1, 2, ..., 11}", ?"gender": "{M, F}"}
[GET] /api/samples/ -> [{"id": "<patient_token>", "age_range": "3", "gender": null}]
```
#### Note
Age ranges are as follows:
- 1: [0, 9]
- 2: [10, 19]
...
- 11: [100+]
