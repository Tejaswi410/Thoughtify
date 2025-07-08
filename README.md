# Thoughtify - Anonymous Thought Board

A Django-based web application that allows users to share their thoughts anonymously. Features include daily thoughts, emotion tagging, and sentiment analysis.

## Features

- 🔒 Anonymous posting with unique user codes
- 📝 Daily thought prompts
- 🎭 Emotion tagging system
- 📊 Sentiment analysis
- ♾️ Infinite scroll feed
- 🎨 Modern, responsive UI
- ⚡ Real-time updates with HTMX

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/thoughtify.git
cd thoughtify
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. Run migrations:
```bash
cd anonymous_thought_board
python manage.py migrate
```

6. Create initial data:
```bash
python manage.py setup_initial_data
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Production Deployment

For production deployment, make sure to:

1. Set `DEBUG=False` in your environment
2. Configure a proper database (e.g., PostgreSQL)
3. Use a production-grade server (e.g., Gunicorn)
4. Set up proper static file serving
5. Configure proper security settings

Example production settings:
```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django 4.2
- UI powered by TailwindCSS
- Interactive features with HTMX 