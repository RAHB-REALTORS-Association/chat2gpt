# Build stage
FROM python:3.11-slim-bookworm as builder
WORKDIR /app
# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app

# Define environment variable
ENV NAME=chat2gpt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run server.py when the container launches
CMD ["python", "server.py"]
