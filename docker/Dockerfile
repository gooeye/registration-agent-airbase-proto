# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container
COPY app/ /app/app/

# Create directories for uploads and processed files
RUN mkdir -p /app/uploads
RUN mkdir -p /app/processed_files

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]