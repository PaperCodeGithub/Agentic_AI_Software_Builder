@echo off

rem Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

rem Run the game
python main.py

pause
