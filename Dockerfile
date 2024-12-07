FROM python:3.12-slim

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
RUN pip install --no-cache-dir nltk

RUN python -m nltk.downloader punkt punkt_tab stopwords

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
