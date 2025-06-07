# Use a full Debian-based image with GUI support
FROM python:3.9-slim-bullseye

# Install Tkinter and dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    && apt-get clean

# Set environment variables to support GUI forwarding
ENV DISPLAY=:0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Run your app
CMD ["python", "main.py"]
