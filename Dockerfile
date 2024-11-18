FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /etc/appconf /app/logs

# Copy the rest of the application
COPY . .

# Ensure token and targets.json are in place
# You'll need to handle these securely, possibly using secrets or environment variables
COPY token /etc/appconf/token
COPY targets.json /etc/appconf/targets.json

# Set permissions
RUN chmod 644 /etc/appconf/token /etc/appconf/targets.json

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "Flask.py"]
