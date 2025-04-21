# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip and install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install netcat for database readiness check
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Make port 80 available to the world outside this container
EXPOSE 8001

# Copy and enable the database wait-for script
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Run the Django migrations and then the development server when the container launches
ENTRYPOINT ["/wait-for-db.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]