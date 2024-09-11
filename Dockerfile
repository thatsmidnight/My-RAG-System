# Base image with Python 3.12
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install project dependencies
RUN pip install \
    --no-cache-dir --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Expose the port the app will run on
EXPOSE 8000

# Start the FastAPI application using gunicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8000"]
