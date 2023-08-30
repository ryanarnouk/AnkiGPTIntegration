# Use Python runtime as base backend runtime
FROM python:3.9

COPY requirements.txt /app/requirements.txt

# Set the working directory within the container
WORKDIR /app

RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 105

ARG open_api_key

ENV OPEN_API_KEY=$open_api_key
ENV DOCKER_RUNTIME True

# Start command
CMD ["python", "api.py"]