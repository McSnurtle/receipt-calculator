@echo on

echo Attempting creation of virtual environment
python3 -m venv venv
.\venv\Scripts\activate

echo Upgrading dependencies
pip install --upgrade --verbose -r requirements.txt

echo Starting app
python3 src/main.py
