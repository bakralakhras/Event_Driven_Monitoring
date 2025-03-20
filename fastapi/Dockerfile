# Use Python as base image
FROM python:3.9

# ENV SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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

# Set working directory inside the container
WORKDIR /app

# Copy only required files first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy all FastAPI project files
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
