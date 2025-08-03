# Dockerfile for Django Bug Tracker
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /src

# Copy requirements.txt into /src
COPY requirements.txt /src/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full project into /src
COPY . /src/

# Expose port for Daphne/ASGI
EXPOSE 8000

# Start Daphne server
CMD ["daphne", "src.bug_tracker.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
