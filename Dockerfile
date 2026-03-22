# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for FAISS, spaCy, and PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model (done already in requirements.txt if using the URL, 
# but redundant is safe if not)
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Expose the API port
EXPOSE 8000

# Start the application using Uvicorn
# We run without --reload for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
