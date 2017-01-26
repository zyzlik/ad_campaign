#!/bin/bash

virtualenv -p python3 venv
source $PWD'/venv/bin/activate'
pip install -r requirements.txt
cd ad_app
python manage.py makemigrations
python manage.py migrate
cd ..
chmod +x ./run.sh
chmod +x ./run_tests.sh