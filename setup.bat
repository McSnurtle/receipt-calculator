@echo off

echo Attempting creation of virtual environment
python3 -m venv venv
call .\venv\Scripts\activate

echo Upgrading dependencies
pip install --upgrade --verbose -r requirements.txt

echo Starting app
:: flask run --app flaskr run --debug
python3 app.py

pause
