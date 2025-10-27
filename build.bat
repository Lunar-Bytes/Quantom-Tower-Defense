@echo off
color 1B

set EXE_NAME=TowerDefense.exe

ECHO [1/5]: Checking for output folder..
if not exist output mkdir output

ECHO [2/5]: Deleting old build folders..
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist main.spec del main.spec
if exist TowerDefense.exe.spec del TowerDefense.exe.spec
if exist TowerDefense.spec del TowerDefense.spec

ECHO [3/5]: Building EXE using pyinstaller..
pyinstaller --noconfirm --onefile --windowed ^
--distpath output ^
--name %EXE_NAME% ^
--add-data "levels;levels" ^
--add-data "assets;assets" ^
--add-data "classes;classes" ^
--add-data "utils;utils" ^
--add-data "config.py;." ^
--add-data "level_select.py;." ^
main.py

ECHO [4/5]: Deleting new build folders..
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist main.spec del main.spec
if exist TowerDefense.exe.spec del TowerDefense.exe.spec
if exist TowerDefense.spec del TowerDefense.spec

ECHO [5/5]: Done! Check 'output' folder!
pause