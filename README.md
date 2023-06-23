# django_sns_app

## activate python venv
source .venv/bin/activate

## deactivate python venv
deactivate

## install python library
pip install -r requirements.txt

## start app
python manage.py runserver

## create Data Table
python manage.py createmigrations
python manage.py migrate

cd snsapp
code admin.py
-> admin.site.register({ table_name })