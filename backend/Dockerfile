# Use an official Python runtime as a parent image
FROM python:3.11.6-slim

# Install system dependencies (if needed, uncomment and modify accordingly)
# RUN apt-get update && apt-get install -y ffmpeg libav-tools && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY . /app

# Create a non-root user and switch to it (uncomment if you want to use a non-root user)
# RUN useradd -m myuser
# USER myuser

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run Gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]