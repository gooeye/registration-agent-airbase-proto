# Use an official Python runtime as a parent image
FROM gdssingapore/airbase:python-3.13
ENV PYTHONBUFFERED=TRUE

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app/ /app/app/

# Change ownership of the /app directory to the 'app' user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE 5000

# Run the application using gunicorn, taking PORT from runtime environment
CMD ["bash", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} app.main:app"]