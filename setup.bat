@echo off
echo Setting up Thoughtify development environment...

REM Create and activate virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run setup script
echo Running setup script...
python setup.py

REM Run migrations
echo Running migrations...
cd anonymous_thought_board
python manage.py makemigrations
python manage.py migrate

echo.
echo Setup completed!
echo.
echo To start the development server:
echo 1. Make sure you're in the 'anonymous_thought_board' directory
echo 2. Run: python manage.py createsuperuser
echo 3. Run: python manage.py runserver
echo.
pause 