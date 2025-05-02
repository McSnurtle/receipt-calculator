@echo off

echo Attempting creation of virtual environment
python3 -m venv venv
call .\venv\Scripts\activate

echo Fetching and upgrading dependencies
pip install --upgrade --verbose -r requirements.txt

echo Initializing django project
django-admin startproject receiptcalculator
cd receiptcalculator

echo Starting local server in development mode
:: flask run --app flaskr run --debug
python3 manage.py runserver 

cd ..
pause
