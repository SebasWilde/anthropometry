# AntroSport

Setup Environment

    mkvirtualenv --python=/usr/bin/python3 antropometry

Install Project

    git clone git clone https://github.com/SebasWilde/anthropometry.git
    cd antropometry
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    python manage.py runserver --settings=antropometry.settings.local
    
Fixtures for each Model

    python manage.py dumpdata root.<model_name> --indent 2 > fixtures/<model_name>.json
    python manage.py loaddata fixtures/*.json

Global Fixtures

    python manage.py dumpdata > backup.json
    python manage.py loaddata backup.json
    
Heroku update

    git add .
    git commit -m 'Commit message'
    git push heroku master

Heroku apply migrations
    
    heroku run bash
    Run commands
    exit(control + d)