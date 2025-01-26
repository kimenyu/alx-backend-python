# Use Python 3.10 as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Avoids writing .pyc files
ENV PYTHONUNBUFFERED 1        # Forces Python output to stdout/stderr

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements to install dependencies first (improves build caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port Django runs on (default 8000)
EXPOSE 8000

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
