#!/bin/bash

echo "Attempting creation of virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "Fetching and upgrading dependencies"
pip install --upgrade --verbose -r requirements.txt

echo "Starting application"
python3 src/main.py

deactivate
read -n1 -r -p "Press any key to continue . . ." key
