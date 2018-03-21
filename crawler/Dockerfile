# Use an official Python runtime as parent image
FROM python:3.5-slim

# Set the working directory to /web_app
WORKDIR /crawler

# Copy the current directory contents into the container at /web_app
ADD . /crawler

# Run web_app.py when the container launches
CMD ["python3", "crawler.py"]