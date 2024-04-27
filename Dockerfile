# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Prevent Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Avoid buffering output from Python to make container logs easier to read
ENV PYTHONUNBUFFERED=1

# Set the port number that the Streamlit app will use
EXPOSE 8080

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code into the container
COPY vivavoce.py /app/vivavoce.py


# Set the working directory and specify the entry point
WORKDIR /app
ENTRYPOINT ["streamlit", "run", "vivavoce.py", "--server.port=8080", "--server.address=0.0.0.0"]
