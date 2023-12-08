echo "Create new AOC day from template"

if "%1"=="" (
  echo "Run with the day number as the first argument:"
  echo "Usage: new.bat <number>"
  exit /b 1
)

set daynumber=%1
set dayname=day%daynumber%

if exist %dayname% (
  echo "Directory %dayname% already exists"
  exit /b 1
)

echo "Creating directory %dayname%"
mkdir %dayname%
echo "Copy template file %dayname%\%dayname%.py"
copy TEMPLATE.py %dayname%\%daynumber%.py