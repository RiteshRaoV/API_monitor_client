# Use official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ../requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-deps -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files for Nginx
RUN python manage.py collectstatic --noinput

# Expose port 8000 where Gunicorn listens
EXPOSE 8000

# Run Gunicorn with config file
CMD ["gunicorn", "-c", "gunicorn.config.py", "api_monitor_client.wsgi:application"]