Write-Host "Setting up Thoughtify development environment..." -ForegroundColor Green

# Create and activate virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run setup script
Write-Host "Running setup script..." -ForegroundColor Yellow
python setup.py

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Yellow
Set-Location -Path "anonymous_thought_board"
python manage.py makemigrations
python manage.py migrate

Write-Host "`nSetup completed!" -ForegroundColor Green
Write-Host "`nTo start the development server:" -ForegroundColor Cyan
Write-Host "1. Make sure you're in the 'anonymous_thought_board' directory"
Write-Host "2. Run: python manage.py createsuperuser"
Write-Host "3. Run: python manage.py runserver`n"

Read-Host "Press Enter to exit" 