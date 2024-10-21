@echo off
echo Create new AOC day from template

if "%1"=="" (
  echo Run with the day number as the first argument:
  echo Usage: new.bat year number
  exit /b 1
)

if "%2"=="" (
  echo Run with the day number as the first argument:
  echo Usage: new.bat year number
  exit /b 1
)

set year=%1
set daynumber=%2
set dayname=day%daynumber%
set daydir=%year%\%dayname%

if exist %daydir% (
  echo Directory %dayname% already exists
  exit /b 1
)

echo Creating directory %daydir%
mkdir %daydir%
echo Copy template file %daydir%\%dayname%.py
copy TEMPLATE.py %daydir%\%daynumber%.py

call set_pythonpath.bat
cd %daydir%
