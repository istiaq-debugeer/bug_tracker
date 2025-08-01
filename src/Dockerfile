# Dockerfile for Django Bug Tracker
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (if any)
# RUN python manage.py collectstatic --noinput

# Expose port for Daphne/ASGI
EXPOSE 8000

# Start Daphne server
CMD ["daphne", "bug_tracker.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
