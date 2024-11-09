@echo off
echo Create new AOC day from template

if "%1"=="" (
  goto :usage
)

if "%2"=="" (
  goto :usage
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
copy templates\TEMPLATE.py %daydir%\%daynumber%.py
echo Copy template file %daydir%\%dayname%.go
copy templates\TEMPLATE.go %daydir%\%daynumber%.go
echo Copy template file %daydir%\%dayname%.ml
copy templates\TEMPLATE.ml %daydir%\day%daynumber%.ml
copy templates\dune-project %daydir%\dune-project
echo (executable (name day%daynumber% )) > %daydir%\dune


call set_pythonpath.bat
rem cd %daydir%
exit /b 0

:usage
echo Usage: new.bat year number
echo Example: new.bat 2020 1
exit /b 1
