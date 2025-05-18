FROM python:3.12-slim

# Set NLTK data directory environment variable
# This tells NLTK where to look for data and where the download script should save it.
ENV NLTK_DATA=/usr/local/nltk_data

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    libffi-dev \
    libssl-dev \
    curl \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install Python primary dependencies with pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install NLTK and download necessary resources
# Install NLTK itself first.
RUN pip install --no-cache-dir nltk

# Copy the NLTK download script into the container
COPY download_nltk_data.py .

# Download NLTK data using the script
# Run the Python script to download the required NLTK data packages.
# This step replaces the problematic `python -m nltk.downloader` command.
RUN python download_nltk_data.py

# Downloading this way sometimes fails, so I used the script instead.
# RUN python -m nltk.downloader punkt punkt_tab stopwords

# Install additional Python dependencies with --only-binary option for efficiency
RUN pip install --no-cache-dir numpy pandas --only-binary=:all:

RUN pip install --no-cache-dir tokenizers

RUN pip install --no-cache-dir bertopic[all]

# Install the rest of the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables for flexibility
ENV HOST=0.0.0.0
ENV PORT=8050

EXPOSE $PORT

# Command to run the application
CMD ["python", "app.py", "--host=${HOST}", "--port=${PORT}"]

# Build and run the Docker container
# docker build --no-cache -t public-tender-analysis-dashboard .
# docker-compose up -d
