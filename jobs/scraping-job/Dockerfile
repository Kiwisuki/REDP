# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt .
COPY src/scraping_job ./src/scraping_job

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Python path to include the current directory
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "-m", "src.scraping_job.main"]
