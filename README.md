# FastAPI Web Application

A modern web application built with FastAPI, featuring both frontend and API components with authentication and persistent storage.

## Features

- FastAPI backend with automatic API documentation
- Jinja2 templating for server-side rendering
- Modern responsive UI with CSS
- JavaScript for dynamic content loading
- RESTful API endpoints
- User authentication with JWT tokens
- Client-side localStorage for persistent auth
- TinyDB for persistent data storage

## Project Structure

```
├── app
│   ├── models        # Data models and schemas
│   ├── routers       # API and page routes
│   └── services      # Business logic and services
├── data              # TinyDB database files
├── static
│   ├── css           # CSS stylesheets
│   └── js            # JavaScript files
├── templates         # HTML templates
├── main.py           # Application entry point
└── requirements.txt  # Project dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment and activate it:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:

```bash
python main.py
```

Or use Uvicorn directly:

```bash
uvicorn main:app --reload
```

Navigate to [http://localhost:8000](http://localhost:8000) in your web browser.

## Authentication

The application includes a complete authentication system:

- User registration at `/register`
- User login at `/login`
- User profile at `/profile`
- JWT token-based authentication
- localStorage for persistent sessions

Authentication flow:
1. User registers with username, email, and password
2. User logs in with credentials
3. Backend validates and returns a JWT token
4. Frontend stores token and user data in localStorage
5. Token is used for authenticated API requests

## Data Persistence

The application uses TinyDB for data storage:

- User accounts are stored in the database
- Items and other data are persisted between server restarts
- Data is stored in JSON format in the `data/` directory

## API Documentation

FastAPI generates interactive API documentation automatically:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Development

To add new API endpoints, create route handlers in the appropriate files in the `app/routers` directory.

To add new pages, create templates in the `templates` directory and add routes in `app/routers/pages.py`.