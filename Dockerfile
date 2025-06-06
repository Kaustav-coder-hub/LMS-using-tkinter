FROM python:3.9-slim

# Set display env for Tkinter to work with X11
ENV DISPLAY=:0

# Install tkinter and X11 tools
RUN apt-get update && \
    apt-get install -y python3-tk libx11-6 && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
