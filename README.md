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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django 4.2
- UI powered by TailwindCSS
- Interactive features with HTMX 
