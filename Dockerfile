# Use official Python image with version 10.12
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/

# Install system dependencies required for FAISS, ChromaDB
RUN apt-get update && \
    apt-get install -y build-essential curl git && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the FastAPI app code
COPY ./app /app/app

# Expose the port FastAPI will run on
EXPOSE 8000

RUN pip install protobuf==3.20
RUN python3 -m spacy download en_core_web_sm

# Command to run FastAPI app
CMD ["sh", "-c", "cd app && uvicorn main:app --host 0.0.0.0 --port 8000"]
