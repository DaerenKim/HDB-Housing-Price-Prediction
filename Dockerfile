# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage caching
COPY requirements.txt .

# Install system dependencies (needed for CatBoost, LightGBM, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose default Streamlit port
EXPOSE 8501

# Make ENTRYPOINT flexible: pass the app filename at runtime
ENTRYPOINT ["streamlit", "run"]
