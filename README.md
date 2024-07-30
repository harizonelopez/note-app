# Flask Notes Application

This is a simple Flask application that allows users to register, log in, and manage personal notes. The application uses SQLite for the database and Flask-WTF for form handling with CSRF protection.

## Features

- User registration
- User login and logout
- Add and delete notes
- CSRF protection

## Requirements

- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Werkzeug

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/harizonelopez/flask-notes-app.git
    cd flask-notes-app
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Mac use `venv\bin\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install Flask Flask-SQLAlchemy Flask-WTF Werkzeug
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Open your web browser and go to `http://127.0.0.1:5000`
