@echo off
TITLE Elemental Creatures Battle Launcher

ECHO ==================================================
ECHO  Welcome to Elemental Creatures Battle!
ECHO ==================================================
ECHO.
ECHO This script will launch the game.
ECHO Make sure you have installed the required libraries by running:
ECHO pip install -r requirements.txt
ECHO.
ECHO Starting game now...
ECHO.

REM Navigate to the directory containing the game's source code
cd code

REM Run the main game file
python main.py

ECHO.
ECHO Game has been closed. Thank you for playing!
ECHO Press any key to exit this window.
pause > nul
