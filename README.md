# Sample Flask Application - Task Manager API

A simple Flask REST API for managing tasks, created to demonstrate AI TestGen pipeline.

## Features

- Create, read, update, delete tasks
- User authentication
- RESTful API endpoints
- SQLite database

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## API Endpoints

- `GET /` - Health check
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## AI TestGen Integration

This project uses AI TestGen for automatic test generation and coverage gating.

The workflow runs on every push and pull request to ensure code quality.
