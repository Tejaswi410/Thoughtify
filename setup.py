import os
import nltk
from pathlib import Path

def setup():
    # Download required NLTK data
    print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    # Create necessary directories
    base_dir = Path(__file__).resolve().parent
    dirs_to_create = [
        base_dir / 'staticfiles',
        base_dir / 'logs',
    ]

    print("Creating necessary directories...")
    for directory in dirs_to_create:
        directory.mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

    # Create .env file if it doesn't exist
    env_file = base_dir / '.env'
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("""# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=thoughtify_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
""")
        print("Created .env file with default settings")

    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Configure your database settings in .env")
    print("2. Run: python manage.py makemigrations")
    print("3. Run: python manage.py migrate")
    print("4. Run: python manage.py createsuperuser")
    print("5. Run: python manage.py runserver")

if __name__ == '__main__':
    setup() 