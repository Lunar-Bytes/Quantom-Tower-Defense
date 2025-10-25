@echo off
REM -----------------------------------------------------
REM Build Tower Defense Python game into a single EXE
REM Includes classes/, utils/, levels/, assets/, config.py, level_select.py
REM -----------------------------------------------------

set EXE_NAME=TowerDefense.exe

ECHO [1/5]: Checking for pyinstaller folder..
if not exist pyinstaller mkdir pyinstaller

ECHO [2/5]: Deleting old build folders..
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist main.spec del main.spec
if exist TowerDefense.exe.spec del TowerDefense.exe.spec

REM Run PyInstaller with all folders included
ECHO [3/5]: Building EXE using pyinstaller..
pyinstaller --noconfirm --onefile --windowed ^
--distpath pyinstaller ^
--name %EXE_NAME% ^
--add-data "levels;levels" ^
--add-data "assets;assets" ^
--add-data "classes;classes" ^
--add-data "utils;utils" ^
--add-data "config.py;." ^
--add-data "level_select.py;." ^
main.py

REM Clean up build files
ECHO [4/5]: Deleting new build folders..
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist main.spec del main.spec
if exist TowerDefense.exe.spec del TowerDefense.exe.spec

ECHO [5/5]: Done!
pause
