@echo off

echo Attempting creation of virtual environment
python3 -m venv venv
call .\venv\Scripts\activate

echo Fetching and upgrading dependencies
pip install --upgrade --verbose -r requirements.txt

echo Starting local server in development mode
:: flask run --app flaskr run --debug
python3 src/main.py

pause
