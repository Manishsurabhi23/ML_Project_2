FROM python:3.10-slim-bookworm

WORKDIR /app

COPY . /app

# Install AWS CLI and system dependencies
RUN apt-get update -y && \
    apt-get install -y awscli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]