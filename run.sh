#! /bin/sh

python manage.py migrate
python manage.py loaddata seed.json

/bin/sh -c 'python manage.py runserver 0.0.0.0:8000'
