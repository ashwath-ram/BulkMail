# Bulk Email System

# 1. Create Virtual Env
- python -m venv env


# 2. activate Environment
- env\Scripts\activate


# 3. Install Packages
pip install -r requirements.txt


# 4. Run (3 terminals)
- python manage.py runserver
- docker run -d -p 6379:6379 redis # redis is not available in windows
- celery -A BulkMail worker -l info --pool=solo
- celery -A BulkMail beat --loglevel=info


# Project URLs
- http://localhost:8000/admin/
Use username - ashwath
    password - 0000

- http://localhost:8000/ [Dashboard]
- http://localhost:8000/campaign/create/
- http://localhost:8000/campaign/list/
- http://localhost:8000/3/  [campaign Logs]


### No Authentication or Authorization 

## using import export package of django for bulk upload of recepients

## pushed .env for validation
