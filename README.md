# receipt-calculator
A simple tkinter application written in python to split the bill of any receipt. Simply input the items purchased and who they were for.

![demo](https://github.com/user-attachments/assets/63c25379-193c-4cb4-9109-09af9d139e07)


## Installation / Quick Start 🌨️
To install the project, first ensure you have it's sole dependency: [`Python3`](<https://www.python.org/downloads/>). Note that for automatic update checking and downloading

**1.** Clone the project
Press the big green Code button, then click download zip to install the source code, and extract the `.zip` file you download.
Alternatively, you can run `git clone https://github.com/McSnurtle/charter.git` to download the source directly.

**2.** Run the setup wizard
Depending on your platform, run the `setup.sh` or `setup.bat` files accordingly - `.sh` for unix based systems (macOS included), and `.bat` for windows.
This script executes the following commands (with some added juice) if you prefer to do this step manually:

for unix:
```shell
git fetch && git pull origin main \
python -m venv venv \
pip install --upgrade --verbose -r requirements.txt \
source ./venv/bin/activate \
python src/main.py
```

for windows:
```batch
git fetch; git pull origin main \
python -m venv venv \
pip install --upgrade --verbose -r requirements.txt \
call .\venv\Scripts\activate \
python src/main.py
```


## User Manual
STUB
