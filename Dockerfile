# Use official Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main/python ./src/main/python

# Expose Flask port
EXPOSE 5000

# Set entry point
CMD ["python", "src/main/python/app.py"]
