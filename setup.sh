#!/bin/bash

echo "Attempting creation of virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "Upgrading dependencies"
pip install --upgrade --verbose -r requirements.txt

echo "Starting app"
# flask --app flaskr run --debug
python3 app.py
