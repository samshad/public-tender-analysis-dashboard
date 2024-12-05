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

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies with pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

RUN pip install --no-cache-dir nltk

RUN python -m nltk.downloader punkt punkt_tab stopwords

RUN pip install --no-cache-dir numpy pandas --only-binary=:all:

RUN pip install --no-cache-dir tokenizers

RUN pip install --no-cache-dir bertopic[all]

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8050

# Command to run the application
CMD ["python", "app.py", "--host=0.0.0.0", "--port=8050"]


# docker build --network host -t public-tender-visualization .
# docker build --no-cache --network host -t public-tender-visualization .
# docker-compose up -d