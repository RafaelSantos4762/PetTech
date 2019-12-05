release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn PetTech.wsgi
heroku config:set DISABLE_COLLECTSTATIC=1