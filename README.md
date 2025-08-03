
# Bug Tracker


A real-time bug tracking system built with Django, Django REST Framework, Channels (WebSockets), and JWT authentication.

This project uses [Daphne](https://github.com/django/daphne) as the ASGI server for real-time features (Channels/WebSockets).

## Key Topics

- Real-time bug tracking with Django Channels and WebSockets
- JWT authentication for secure API access
- Modular app structure (Projects, Bugs, Comments)
- Activity logging and notifications
- Dockerized for easy deployment
- API documentation with Swagger/Redoc

## Features

- User authentication with JWT
- Project management (CRUD)
- Bug management (CRUD, assign, status, priority)
- Commenting on bugs
- Real-time notifications via WebSockets (Channels + Redis)
- Activity logging
- API documentation with Swagger (drf-yasg)

## Requirements

- Python 3.11+
- Docker & Docker Compose (recommended)
- Redis (for Channels)

## Getting Started

## Clone the repository

```sh
git clone <your-repo-url>
cd bug_tracker
```

### Running with Docker

Build and start the services:

```sh
docker-compose up --build
```

This will:
- Build the Docker image
- Start the Django app with Daphne ASGI server on port 8000
- Mount your code for live reload

### Running Locally (without Docker)

1. Install dependencies:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Start Redis server (required for Channels):

    ```sh
    redis-server
    ```

3. Apply migrations:

    ```sh
    cd src
    python manage.py migrate
    ```

4. Create a superuser (optional):

    ```sh
    python manage.py createsuperuser
    ```

5. Run the development server:

    # Option 1: Run with Django's development server (for basic testing)
    python manage.py runserver

    # Option 2: Run with Daphne for full ASGI support (recommended for Channels/WebSockets)
    # Make sure you are in the src directory
    daphne bug_tracker.asgi:application

    # By default, Daphne will run on 127.0.0.1:8000
    # To specify a port:
    daphne -p 8000 bug_tracker.asgi:application

    # You can also specify the host if needed:
    daphne -b 0.0.0.0 -p 8000 bug_tracker.asgi:application

### API Documentation

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### Authentication: How to Get and Use JWT Token

1. **Obtain a Token:**

    Send a POST request to `/api/token/` with your username and password:

    ```sh
    curl -X POST http://localhost:8000/api/token/ \
      -H 'Content-Type: application/json' \
      -d '{"username": "your_username", "password": "your_password"}'
    ```

    The response will include `access` and `refresh` tokens.

2. **Authenticate with Token:**

    For authenticated API requests, include the access token in the `Authorization` header:

    ```sh
    curl -H "Authorization: Bearer <your_access_token>" http://localhost:8000/api/projects/
    ```

    Replace `<your_access_token>` with the token you received.

3. **Refresh Token:**

    To refresh your access token:

    ```sh
    curl -X POST http://localhost:8000/api/token/refresh/ \
      -H 'Content-Type: application/json' \
      -d '{"refresh": "<your_refresh_token>"}'
    ```

### WebSocket Endpoints

- `/ws/projects/<project_id>/` — Real-time notifications for project events

### Project Structure

```
src/
  manage.py
  bug_tracker/
    settings.py
    urls.py
    asgi.py
    wsgi.py
  tracker/
    models.py
    views.py
    serializers.py
    urls.py
    consumers.py
    routing.py
    utils.py
    ...
```

### Useful Commands

- Run tests:
    ```sh
    python manage.py test tracker
    ```
- Access Django admin:
    - [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Environment Variables

- `DJANGO_SETTINGS_MODULE=bug_tracker.settings` (set automatically in Docker)

## Using PostgreSQL Instead of SQLite

By default, the project uses SQLite for development. To use PostgreSQL:

1. Install PostgreSQL and the Python driver:
    ```sh
    pip install psycopg2-binary
    ```
2. Update your `src/bug_tracker/settings.py` `DATABASES` section:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
3. Apply migrations:
    ```sh
    python manage.py migrate
    ```
4. Update your Docker and environment variables as needed for production.


**Note:**  
- Make sure Redis is running for WebSocket features.
- Update `<repo-url>` with   repository url