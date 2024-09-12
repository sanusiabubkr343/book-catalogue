# Use Python as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and setup.py
COPY frontend_api/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY frontend_api .

# Expose the port the app will run on
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["python", "manage.py", "migrate", "--noinput", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]
