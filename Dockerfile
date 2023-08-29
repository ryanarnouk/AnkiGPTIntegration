# Use Python runtime as base backend runtime
FROM python:3.9

# Set the working directory within the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Start command
CMD ["python", "api.py"]