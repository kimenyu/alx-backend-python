# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /messaging_app

# Copy requirements file into the container
COPY requirements.txt /messaging_app/

RUN pip install --upgrade pip setuptools

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /messaging_app/

# Expose the default Django port
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
